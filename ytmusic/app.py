"""Interfaz gráfica (Tkinter) del descargador de YouTube a MP3/MP4."""

import os
import queue
import subprocess
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from . import downloader
from .storage import APP_NAME, Config, History


def open_folder(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    os.startfile(path)


def reveal_file(path: Path):
    """Abre el Explorador con el archivo seleccionado."""
    subprocess.Popen(["explorer", "/select,", str(path)])


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} – Descargador de YouTube")
        self.geometry("900x580")
        self.minsize(720, 460)

        self.config_data = Config()
        self.history = History()
        self.events = queue.Queue()
        self.busy = False

        self._build_ui()
        self.refresh_history()
        self.after(100, self._poll_events)

    # ---------- UI ----------
    def _build_ui(self):
        style = ttk.Style(self)
        if "vista" in style.theme_names():
            style.theme_use("vista")

        pad = {"padx": 10, "pady": 6}

        # Enlace + formato + botón descargar
        top = ttk.LabelFrame(self, text="Nueva descarga")
        top.pack(fill="x", **pad)

        ttk.Label(top, text="Enlace de YouTube:").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(top, textvariable=self.url_var)
        url_entry.grid(row=0, column=1, columnspan=3, sticky="ew", padx=8, pady=6)
        url_entry.bind("<Return>", lambda e: self.start_download())
        url_entry.focus_set()
        ttk.Button(top, text="Pegar", command=self._paste).grid(row=0, column=4, padx=8)

        ttk.Label(top, text="Formato:").grid(row=1, column=0, sticky="w", padx=8, pady=6)
        self.fmt_var = tk.StringVar(value="mp3")
        ttk.Radiobutton(top, text="MP3 (audio)", value="mp3", variable=self.fmt_var).grid(row=1, column=1, sticky="w", padx=8)
        ttk.Radiobutton(top, text="MP4 (vídeo)", value="mp4", variable=self.fmt_var).grid(row=1, column=2, sticky="w", padx=8)
        self.download_btn = ttk.Button(top, text="Descargar", command=self.start_download)
        self.download_btn.grid(row=1, column=4, padx=8, pady=6)
        top.columnconfigure(3, weight=1)

        # Progreso
        self.progress = ttk.Progressbar(top, mode="determinate", maximum=100)
        self.progress.grid(row=2, column=0, columnspan=5, sticky="ew", padx=8, pady=(4, 2))
        self.status_var = tk.StringVar(value="Listo.")
        ttk.Label(top, textvariable=self.status_var).grid(row=3, column=0, columnspan=5, sticky="w", padx=8, pady=(0, 6))

        # Carpeta de descargas
        folder = ttk.LabelFrame(self, text="Carpeta de descargas")
        folder.pack(fill="x", **pad)
        self.folder_var = tk.StringVar(value=str(self.config_data.download_dir))
        ttk.Entry(folder, textvariable=self.folder_var, state="readonly").pack(side="left", fill="x", expand=True, padx=8, pady=6)
        ttk.Button(folder, text="Cambiar…", command=self.change_folder).pack(side="left", padx=4, pady=6)
        ttk.Button(folder, text="📂 Abrir carpeta", command=lambda: open_folder(self.config_data.download_dir)).pack(side="left", padx=8, pady=6)

        # Historial
        hist = ttk.LabelFrame(self, text="Historial de descargas")
        hist.pack(fill="both", expand=True, **pad)

        cols = ("fecha", "formato", "titulo", "ruta")
        self.tree = ttk.Treeview(hist, columns=cols, show="headings", selectmode="browse")
        for col, text, width, stretch in (
            ("fecha", "Fecha", 140, False),
            ("formato", "Formato", 70, False),
            ("titulo", "Título", 280, True),
            ("ruta", "Ubicación", 360, True),
        ):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, stretch=stretch, anchor="center" if col == "formato" else "w")
        self.tree.tag_configure("missing", foreground="#a33")
        self.tree.bind("<Double-1>", lambda e: self.reveal_selected())

        scroll = ttk.Scrollbar(hist, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=6)
        scroll.grid(row=0, column=1, sticky="ns", pady=6, padx=(0, 8))
        hist.rowconfigure(0, weight=1)
        hist.columnconfigure(0, weight=1)

        buttons = ttk.Frame(hist)
        buttons.grid(row=1, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 8))
        ttk.Button(buttons, text="Mostrar en carpeta", command=self.reveal_selected).pack(side="left")
        ttk.Button(buttons, text="Reproducir / abrir", command=self.open_selected).pack(side="left", padx=6)
        ttk.Button(buttons, text="Quitar del historial", command=self.delete_selected).pack(side="left")
        ttk.Button(buttons, text="Exportar CSV…", command=self.export_csv).pack(side="right")

    # ---------- Acciones ----------
    def _paste(self):
        try:
            self.url_var.set(self.clipboard_get().strip())
        except tk.TclError:
            pass

    def change_folder(self):
        chosen = filedialog.askdirectory(initialdir=self.config_data.download_dir, title="Elige la carpeta de descargas")
        if chosen:
            self.config_data.download_dir = Path(chosen)
            self.folder_var.set(str(self.config_data.download_dir))

    def start_download(self):
        if self.busy:
            return
        url = self.url_var.get().strip()
        if not downloader.is_youtube_url(url):
            messagebox.showwarning(APP_NAME, "Introduce un enlace válido de YouTube.")
            return
        fmt = self.fmt_var.get()
        out_dir = self.config_data.subdir(fmt)

        self.busy = True
        self.download_btn.configure(state="disabled")
        self.progress.configure(value=0)
        threading.Thread(target=self._worker, args=(url, fmt, out_dir), daemon=True).start()

    def _worker(self, url, fmt, out_dir):
        try:
            title, path = downloader.download(
                url,
                fmt,
                out_dir,
                on_progress=lambda pct, text: self.events.put(("progress", pct, text)),
                on_status=lambda text: self.events.put(("status", text)),
            )
            self.events.put(("done", title, fmt, url, path))
        except Exception as exc:  # noqa: BLE001 - mostramos cualquier fallo al usuario
            self.events.put(("error", str(exc)))

    def _poll_events(self):
        try:
            while True:
                event = self.events.get_nowait()
                kind = event[0]
                if kind == "progress":
                    _, pct, text = event
                    if pct is None:
                        self.progress.configure(mode="indeterminate")
                        self.progress.step(2)
                    else:
                        self.progress.configure(mode="determinate", value=pct)
                    self.status_var.set(text)
                elif kind == "status":
                    self.status_var.set(event[1])
                elif kind == "done":
                    _, title, fmt, url, path = event
                    self.history.add(title, fmt.upper(), url, path)
                    self.refresh_history()
                    self.progress.configure(mode="determinate", value=100)
                    self.status_var.set(f"✔ Descargado: {path}")
                    self.url_var.set("")
                    self._finish()
                elif kind == "error":
                    self.progress.configure(mode="determinate", value=0)
                    self.status_var.set("Error en la descarga.")
                    messagebox.showerror(APP_NAME, f"No se pudo descargar:\n\n{event[1]}")
                    self._finish()
        except queue.Empty:
            pass
        self.after(100, self._poll_events)

    def _finish(self):
        self.busy = False
        self.download_btn.configure(state="normal")

    # ---------- Historial ----------
    def refresh_history(self):
        self.tree.delete(*self.tree.get_children())
        for entry_id, fecha, titulo, formato, _url, ruta in self.history.all():
            tags = () if Path(ruta).exists() else ("missing",)
            self.tree.insert("", "end", iid=str(entry_id), values=(fecha, formato, titulo, ruta), tags=tags)

    def _selected_path(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo(APP_NAME, "Selecciona una descarga del historial.")
            return None
        path = Path(self.tree.set(sel[0], "ruta"))
        if not path.exists():
            messagebox.showwarning(APP_NAME, f"El archivo ya no existe:\n{path}")
            return None
        return path

    def reveal_selected(self):
        path = self._selected_path()
        if path:
            reveal_file(path)

    def open_selected(self):
        path = self._selected_path()
        if path:
            os.startfile(path)

    def delete_selected(self):
        sel = self.tree.selection()
        if sel and messagebox.askyesno(APP_NAME, "¿Quitar esta entrada del historial? (el archivo no se borra)"):
            self.history.delete(int(sel[0]))
            self.refresh_history()

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")], initialfile="historial_descargas.csv"
        )
        if path:
            self.history.export_csv(Path(path))
            messagebox.showinfo(APP_NAME, f"Historial exportado a:\n{path}")


def main():
    App().mainloop()
