"""Descarga de YouTube en MP3 o MP4 usando yt-dlp."""

import re
from pathlib import Path

import imageio_ffmpeg
import yt_dlp

YOUTUBE_RE = re.compile(r"^(https?://)?(www\.|m\.|music\.)?(youtube\.com|youtu\.be)/", re.I)


def is_youtube_url(url: str) -> bool:
    return bool(YOUTUBE_RE.match(url.strip()))


class _QuietLogger:
    def debug(self, msg):
        pass

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


def download(url: str, fmt: str, out_dir: Path, on_progress=None, on_status=None):
    """Descarga `url` en `fmt` ("mp3" o "mp4") dentro de `out_dir`.

    on_progress(porcentaje: float | None, texto: str) y on_status(texto: str) son
    callbacks opcionales (se llaman desde el hilo de descarga).
    Devuelve (titulo, ruta_final).
    """
    fmt = fmt.lower()
    final_path = {}

    def progress_hook(d):
        if not on_progress:
            return
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            done = d.get("downloaded_bytes", 0)
            pct = done * 100 / total if total else None
            speed = d.get("_speed_str", "").strip()
            eta = d.get("_eta_str", "").strip()
            on_progress(pct, f"Descargando… {speed}  ETA {eta}".strip())
        elif d["status"] == "finished":
            on_progress(100, "Procesando archivo…")

    def postprocessor_hook(d):
        if d["status"] == "finished":
            path = d.get("info_dict", {}).get("filepath")
            if path:
                final_path["path"] = path

    opts = {
        "outtmpl": str(out_dir / "%(title)s [%(id)s].%(ext)s"),
        "windowsfilenames": True,
        "noplaylist": True,
        "ffmpeg_location": imageio_ffmpeg.get_ffmpeg_exe(),
        "progress_hooks": [progress_hook],
        "postprocessor_hooks": [postprocessor_hook],
        "logger": _QuietLogger(),
        "noprogress": True,
    }

    if fmt == "mp3":
        opts.update(
            format="bestaudio/best",
            postprocessors=[
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"},
                {"key": "FFmpegMetadata"},
            ],
        )
    elif fmt == "mp4":
        opts.update(
            # Preferimos H.264 + AAC: se reproduce en cualquier reproductor de Windows
            format="bv*[vcodec^=avc1]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b",
            merge_output_format="mp4",
            postprocessors=[{"key": "FFmpegMetadata"}],
        )
    else:
        raise ValueError(f"Formato no soportado: {fmt}")

    if on_status:
        on_status("Obteniendo información del vídeo…")

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        info = ydl.sanitize_info(info)

    path = final_path.get("path")
    if not path:
        downloads = info.get("requested_downloads") or []
        path = downloads[-1].get("filepath") if downloads else None
    if not path:
        raise RuntimeError("No se pudo determinar la ruta del archivo descargado.")

    return info.get("title") or Path(path).stem, str(Path(path).resolve())
