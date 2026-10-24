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

## Instalar en cualquier PC (sin Python ni git)

1. Descarga `YTMusic-Setup-x.y.z.exe` de la sección
   [Releases](https://github.com/Alexjmendez/YTMusic/releases).
2. Ejecútalo y sigue el asistente (no necesita permisos de administrador).
   Crea accesos directos en el menú Inicio y, opcionalmente, en el escritorio.
3. Para desinstalar: *Configuración → Aplicaciones → YTMusic → Desinstalar*.

> Windows SmartScreen puede avisar porque el instalador no está firmado:
> pulsa *Más información → Ejecutar de todas formas*.

## Ejecutar desde el código fuente

1. Instala Python 3.10+ desde <https://www.python.org/downloads/> marcando
   *Add python.exe to PATH*.
2. Doble clic en `ejecutar.bat` (la primera vez crea el entorno e instala dependencias).

Si YouTube deja de funcionar, normalmente basta con actualizar yt-dlp
(`ejecutar.bat` lo hace en cada arranque). En la versión instalada hay que
generar e instalar un instalador nuevo.

## Crear el instalador

Requiere [Inno Setup 6](https://jrsoftware.org/isinfo.php)
(`winget install JRSoftware.InnoSetup`). Doble clic en `crear_instalador.bat`
→ `dist\YTMusic-Setup-x.y.z.exe`. La versión se cambia en `installer.iss`.

> Descarga solo contenido del que tengas derechos o permiso, respetando los
> términos de servicio de YouTube.
