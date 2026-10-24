"""Configuración, carpeta de descargas e historial (SQLite)."""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

APP_NAME = "YTMusic"

# Datos de la app (config + historial) en %APPDATA%\YTMusic
DATA_DIR = Path(os.environ.get("APPDATA", Path.home())) / APP_NAME
CONFIG_FILE = DATA_DIR / "config.json"
DB_FILE = DATA_DIR / "historial.db"

# Carpeta de descargas por defecto: %USERPROFILE%\Music\YTMusic
DEFAULT_DOWNLOAD_DIR = Path.home() / "Music" / APP_NAME


class Config:
    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._data = {"download_dir": str(DEFAULT_DOWNLOAD_DIR)}
        if CONFIG_FILE.exists():
            try:
                self._data.update(json.loads(CONFIG_FILE.read_text(encoding="utf-8")))
            except (OSError, ValueError):
                pass
        self.ensure_dirs()

    @property
    def download_dir(self) -> Path:
        return Path(self._data["download_dir"])

    @download_dir.setter
    def download_dir(self, value):
        self._data["download_dir"] = str(value)
        self.ensure_dirs()
        self.save()

    def subdir(self, fmt: str) -> Path:
        """Subcarpeta por formato: ...\\MP3 o ...\\MP4."""
        path = self.download_dir / fmt.upper()
        path.mkdir(parents=True, exist_ok=True)
        return path

    def ensure_dirs(self):
        for fmt in ("mp3", "mp4"):
            (self.download_dir / fmt.upper()).mkdir(parents=True, exist_ok=True)

    def save(self):
        CONFIG_FILE.write_text(json.dumps(self._data, indent=2, ensure_ascii=False), encoding="utf-8")


class History:
    def __init__(self, db_path: Path = DB_FILE):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS descargas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                titulo TEXT,
                formato TEXT NOT NULL,
                url TEXT NOT NULL,
                ruta TEXT NOT NULL
            )"""
        )
        self.conn.commit()

    def add(self, titulo: str, formato: str, url: str, ruta: str) -> int:
        cur = self.conn.execute(
            "INSERT INTO descargas (fecha, titulo, formato, url, ruta) VALUES (?, ?, ?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), titulo, formato, url, ruta),
        )
        self.conn.commit()
        return cur.lastrowid

    def all(self):
        return self.conn.execute(
            "SELECT id, fecha, titulo, formato, url, ruta FROM descargas ORDER BY id DESC"
        ).fetchall()

    def delete(self, entry_id: int):
        self.conn.execute("DELETE FROM descargas WHERE id = ?", (entry_id,))
        self.conn.commit()

    def export_csv(self, path: Path):
        import csv

        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["id", "fecha", "titulo", "formato", "url", "ruta"])
            writer.writerows(self.all())
