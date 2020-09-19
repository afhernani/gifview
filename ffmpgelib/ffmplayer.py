#!/usr/bin/env python3
import os, sys, io
import threading
from ffpyplayer.player import MediaPlayer
# from ffpyplayer.pic import Image as PicImage
import time
from PIL import Image, ImageTk

__author__ = 'Hernani Aleman Ferraz'
__email__ = 'afhernani@gmail.com'
__apply__ = 'console - ffpyplayer with Image PIL'
__version__ = '1'
__all__ = ('MediaImage')

class MediaImage:
    _player = None
    def __init__(self, url=None):
        self.imgs = []
        self.status = True
        self.url = None if url is None else url
        ff_opts = {'paused': True, 'autoexit': False, 
                   'autorotate': False, 'volume': 0.5,
                   'filter_threads': 4 }  # Audio options
        try:
            self._player = MediaPlayer(self.url, ff_opts=ff_opts)
            ti = time.process_time()
            time_fin = 1.50
            while self._player.get_metadata()['src_vid_size'] == (0, 0):
                t = time.process_time()-ti
                if t >= time_fin:
                    raise Exception("can't open " + url)
            self.metadata  = self._player.get_metadata()
        except Exception as e:
            print(str(e.args))
            self.status = False
        # print(self.metadata)
    
    def extract(self, ni=0, w=-1, h=-1, save=True):
        '''
            Extract Images from url video.
            parameters:
                int, ni = 0, total images to extract
                int, w=-1  new width images, default proportion
                int, h=-1  new height images, default proportion
                bool, save=True, save images as gif is true
        '''
        ti = time.process_time()
        self.imgs.clear()
        if ni == 0: return
        pts = self.metadata['duration'] / (ni + 1)
        # self._player.set_size(self, int width=-1, int height=-1) # set imagen return for player
        if self._player.get_pause(): self._player.toggle_pause()
        if w != -1 or h != -1:
            self._player.set_size(width=w,height=h)
            while True:
                frame, val = self._player.get_frame()
                if frame:
                    if frame[0]:
                        if  w != -1 and frame[0].get_size()[0] == w:
                            break
                        elif h != -1 and frame[0].get_size()[1] == h:
                            break 
        for i in range(ni):
            frame = None
            self._player.seek(pts=pts, relative=True, accurate=False)
            time.sleep(0.03)
            while frame is None:
                frame, val = self._player.get_frame()
                # time.sleep(0.03)
                print(val)
                if val == 'eof':
                    break
            img, t = frame
            print(pts, val, t, img.get_pixel_format(), img.get_buffer_size())
            data = img.to_memoryview()[0].memview
            image = Image.frombytes(mode='RGB', size=img.get_size(), data=data)
            self.imgs.append(image)
            time.sleep(val)
            
        self._player.toggle_pause()
        if save and len(self.imgs)>=1:
            self.savegif()
        print('time:', time.process_time()-ti, 'sg')

    def savegif(self, name=''):
        name_video = os.path.basename(self.url)
        dir_video = os.path.dirname(self.url)
        dir_thumb = os.path.join(dir_video, '.Thumbails')
        if not os.path.isdir(dir_thumb):
            os.mkdir(dir_thumb)
        name += name_video + '_nfx_.gif'
        name_thumb = os.path.join(dir_thumb, name)
        self.imgs[0].save(name_thumb,
               save_all=True,
               append_images=self.imgs[1:],
               duration=1000,
               loop=0)
    
    @staticmethod
    def whichWH(imgs=[])-> tuple:
        ''' get (w, h) maxima from a group of images
            parameters:
                imgs=[] : list of images
            return
                tuple size = w,h : maximum or 0, 0 it is not posible
        '''
        import types
        z = 0, 0
        if len(imgs) >= 1:
            try:
                if isinstance(imgs[0].size, tuple):
                    w, h = 0, 0
                    for itm in imgs:
                        if w < itm.size[0]:
                            w = itm.size[0]
                        if h < itm.size[1]:
                            h = itm.size[1]
                    z = w, h
            except AttributeError as e:
                print(str(e.args))
        return z

    # interfaz iterable for class MediaImage
    def __iter__(self):
        return MediaIterator(self.imgs)

    # Release the video source when the object is destroyed
    def __del__(self):
        self._player.close_player()
        # print('__del__')


class MediaIterator:
    ''' Iterator class '''
    def __init__(self, imgs=[]):
        # imgs object reference
        self._imgs = imgs
        # member variable to keep track of current index
        self._index = 0

    def __next__(self):
        if self._index < len(self._imgs):
            v = self._index
            self._index += 1
            return self._imgs[v]
        else:
            raise StopIteration


if __name__ == '__main__':
    url = '798ed35b46236de51a5e1bd610f92dd5.mp4'
    url1 = 'e32136c2258a4ae31ef5383e58e24154.mp4'
    mediaimage = MediaImage(url=os.path.abspath(url))
    print(mediaimage.metadata)
    
    # mediaimage.extract(9)
    # img = mediaimage.image_from_dataio()
    # img.save('prueba.gif')
    # mediaimage._player.set_size(300, -1)
    # time.sleep(0.03)
    # mediaimage._player.toggle_pause()
    # mediaimage._player.seek(pts = 0.0, relative=False)
    # time.sleep(0.2)
    # mediaimage._player.toggle_pause()
    
    mediaimage.extract(32, w=300, save=False)
    a = 1
    img_x = []
    for item in mediaimage:
        print(a, item)
        a += 1
        img_x.append(item)
    # img = mediaimage.image_from_dataio()
    # img.save('prueba2.gif')
    '''mediaimage.imgs[1].save('prueba3.gif',
               format='gif',
               save_all=True,
               append_images=mediaimage.imgs[2:],
               duration=1000,
               loop=0)'''
    # del mediaimage
    # mediaimage._player.close_player()
    # uno = [1, 2, 3]
    # print(MediaImage.whichWH(imgs=mediaimage.imgs))
    print(MediaImage.whichWH(imgs=img_x))
    del mediaimage
    # mediaimage = None
    # print(type(mediaimage))
    '''try:
        if not mediaimage:
            mediaimage = MediaImage(url=os.path.abspath(url1))
            valor = mediaimage._player.get_metadata()
            print(valor)
            mediaimage.extract(ni=50)
    except Exception as e:
        print('exception:', str(e.args))
        print('tipo:',type(mediaimage._player)) '''
