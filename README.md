# Script GifView
## Edicion, Composicion, Imagenes, Videos

### Construyendo un visor de imagenes GUI en tk, con formato de entrad .gif que son almacenados en un directorio oculto de nombre Thumbails, en el directorio base de los archivos de video del path raiz. Los ficheros de videos pueden ser de los formatos más comunes, .mp4, .flv, .avi, ... etc,. Los thumbails de los videos de raiz se pueden crear utilizando la aplicacion GUIMovieToGif, así, obtenemos un visor gifview que enlaza con los videos correspondientes en los archivos de raiz designado.

#### Lanzar:

Usage: python movie2gif

# GUIMovieToGif
## Entorno GUI de biblioteca Tk.
### Con un entorno amigable seleccionamos el directorio donde se almacenan los  ficheros de video, seleccinamos el fichero a extraer, y click en make para crea un gif de 5 imagenes con formato original que se escala a un ancho de 200 pixel y altura proporcional.
### Mejoras:
	+ Dotarlo de subtareas para la extracción
	+ Menu obciones con el numero de imagnes a extraer, una imagen especifica, y formato de salida..

### Dependencias:
	Se requiere tener instalado la aplicacion ffmpeg en el sistema, y configurada las rutas del mimo, ver: https://ffmpeg.org, 

# autogif.py
## Entorno GUI de biblioteca Tk.
### Con un entorno amigable seleccionamos el directorio donde se almacenan los  ficheros de video, picamos en make y automáticamente construye todos los gif pertenecientes a los ficheros que estén incluidos en el directorio seleccionado.
### Mejoras:
	+ Dotado de subtareas para la extracción
    + Posee una pausa, para no sobrecargar el sitema (5 seg) que da un retrazo en la actualización del gui
	+ Menu obciones con el numero de imagnes a extraer, una imagen especifica, y formato de salida..

### Dependencias:
	Se requiere tener instalado la aplicacion ffmpeg en el sistema, y configurada las rutas del mimo, ver: https://ffmpeg.org, 