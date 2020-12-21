# App GifView for dinamic  v.3.2
## Edicion, Composicion, Imagenes, Videos

### Construyendo un visor de imagenes GUI en tk, con formato de entrad .gif que son almacenados en un directorio oculto de nombre .Thumbails, en el directorio base de los archivos de video del path raiz. Los ficheros de videos pueden ser de los formatos más comunes, .mp4, .flv, .avi, ... etc,. Los thumbails de los videos de raiz se pueden crear utilizando la aplicacion MediaPlayer del packg ffpyplayer, así, como la clase MediaImagen del packgage ffmpgelib, incluida en gifview, con el que  obtenemos un conjunto de imagenes, creando el gif. el visor gifview enlaza con los videos correspondientes en los archivos de raiz designado.

#### Lanzar:

Usage: python flowlayout.py

### Mejoras:
    + Configuracion parametros tamaño split's.
	+ Dotarlo de subtareas para la extracción
	+ Menu obciones con el numero de imagnes a extraer, una imagen especifica, y formato de salida..

### Dependencias:
	Se requiere tener instalado la aplicacion ffmpeg en el sistema, y configurada las rutas del mimo, ver: https://ffmpeg.org, 
	- tkinter GUI python3
	- ffpyplayer
	- PIL