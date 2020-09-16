"""
ffmpeglib package.
Usefull extensions of the ffpyplayer and PIL Image extract

Package Structure
=================

Modules:

* __init__.py: API imports

"""
__author__ = 'hernani'
__version__ = 'ffmpeglib-0.0.1'

try:
    from .ffmplayer import MediaImage
except:
    from ffmplayer import MediaImage


