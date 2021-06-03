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
__apply__ = 'console - Mediaplayer with Image PIL'
__version__ = '1'

try:
    from .ffmplayer import MediaImage
    from .graphicblock import Graphics
    from .imageblock import ImageBlock
    from .ToolTip import ToolTip, createToolTip
    from .tooltipmenu import ToolTipMenu, createToolTipMenu
    from .windialog impor LabelEntryButton, FrameButtons,
            WindowCopyTo, CustomEntry, WindowCopyTo, ToolFile
except ImportError:
    from ffmplayer import MediaImage
    from graphicblock import Graphics
    from imageblock import ImageBlock
    from ToolTip import ToolTip, createToolTip
    from tooltipmenu import ToolTipMenu, createToolTipMenu
    from windialog impor LabelEntryButton, FrameButtons,
            WindowCopyTo, CustomEntry, WindowCopyTo, ToolFile


