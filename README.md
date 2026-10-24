# YTMusic – Descargador de YouTube a MP3 / MP4

Aplicación de escritorio para Windows (Python + Tkinter) que usa la librería
[yt-dlp](https://github.com/yt-dlp/yt-dlp) para descargar vídeos de YouTube como
**MP3** (audio 192 kbps) o **MP4** (vídeo con audio).

## Funciones

- Pega un enlace de YouTube, elige MP3 o MP4 y pulsa **Descargar** (o Enter).
- Barra de progreso con velocidad y tiempo restante.
- **Carpeta gestionada automáticamente**: por defecto `%USERPROFILE%\Music\YTMusic`,
  con subcarpetas `MP3` y `MP4` que se crean solas. Se puede cambiar con **Cambiar…**.
- Botón **📂 Abrir carpeta** para ir directamente a los archivos.
- **Historial** de todas las descargas (fecha, formato, título y ruta del archivo),
  guardado en `%APPDATA%\YTMusic\historial.db`:
  - Doble clic o **Mostrar en carpeta** abre el Explorador con el archivo seleccionado.
  - **Reproducir / abrir** lo abre con la aplicación predeterminada.
  - Las entradas cuyo archivo ya no existe aparecen en rojo.
  - **Exportar CSV…** guarda el historial en un archivo CSV.
- FFmpeg viene incluido vía `imageio-ffmpeg`; no hace falta instalarlo.

## Uso

1. Instala Python 3.10+ desde <https://www.python.org/downloads/> marcando
   *Add python.exe to PATH*.
2. Doble clic en `ejecutar.bat` (la primera vez crea el entorno e instala dependencias).

Para generar un `.exe` independiente: doble clic en `compilar_exe.bat` → `dist\YTMusic.exe`.

Si YouTube deja de funcionar, normalmente basta con actualizar yt-dlp
(`ejecutar.bat` lo hace en cada arranque).

> Descarga solo contenido del que tengas derechos o permiso, respetando los
> términos de servicio de YouTube.
