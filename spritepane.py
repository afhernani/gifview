#!/usr/bin/env python3
# _*_ coding:UTF-8 _*_

import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os, sys, subprocess
from threading import Thread
import ffmpgelib
from ffmpgelib import MediaImage, Graphics
from ffmpgelib import createToolTip
from datetime import timedelta
from ffmpgelib import createToolTipMenu, ToolFile
from ffmpgelib import WindowCopyTo, OpenDialogRename


class SpritePane(tk.Frame):
    def __init__(self, parent, url=None, timer=None, **kargs):
        ''' set init value, 
                parameters:
                    parent: object root, tk.Frame or parent window
                    url: str path to file video.
                    timer: int - time refresh animation
                    **kargs: *parameter parent
        '''
        tk.Frame.__init__(self, parent, **kargs)
        self.parent = parent
        self.url = '' if url is None else url # path viedo
        self.ni = 32 # num de imagenes a extaer.
        self.timer = 850 if timer is None else timer
        # ---
        self.width = 300
        self.height = 220
        # ----
        self.pathdir = tk.StringVar(value = os.path.dirname(self.url)) # dir content video
        self.pathdirthum = tk.StringVar()
        self.name = tk.StringVar()
        self.namethumb = tk.StringVar()
        self.source = ''
        eurl, esou = self.check_exist()
        self.graphics = Graphics()
        self.metadatos = None
        mediaplay = MediaImage(self.url)
        self.metadatos = mediaplay.metadata
        if esou:
            # si los dos existen solo creamos
            del mediaplay
            kv = {'path': self.source, 'transform':True, 
                'width':self.width, 'height':self.height }
            self.graphics.config(**kv)
        elif eurl:
            # imagen de carga de video espera.
            # solo existe el video
            # TODO: desarrollar la extraccion y la adicción
            mediaplay.extract(ni=self.ni, save=True)
            del mediaplay
            kv = {'path': self.source, 'transform':True, 
                'width':self.width, 'height':self.height }
            self.graphics.config(**kv)
        # tooltips -create
        text = str(timedelta(seconds=self.metadatos['duration']))
        createToolTip(self, text)
        # Creamos menu
        self.menu = tk.Menu(self, tearoff=False)
        self.menu.add_command(label="move ...", command=self.move)
        self.menu.add_command(label="copy ...", command=self.copy)
        self.menu.add_command(label="remove ...", command=self.remove)
        self.menu.add_separator()
        self.menu.add_command(label="rename ...", command=self.rename)
        createToolTipMenu(self, self.menu)
        # extraemos imagen:
        self.count = self.graphics.imgBox.count
        self.index = 5
        if self.count:
            self.index = int(self.count / 3)
        self.photo = ImageTk.PhotoImage(self.graphics.getImagenSecuencia(self.index))
        # creamos canvas
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="yellow")
        self.canvas.pack()
        self.image = self.canvas.create_image(self.width/2, self.height/2, image=self.photo)
        self.canvas.bind('<Enter>', self.enter)
        self.canvas.bind('<Leave>', self.leave)
        self.canvas.bind('<Double-Button-1>', self.double_click_canvas)
        self.canvas.bind('<Button-3>', self.my_popup) # make menu
        self.animating = True
        # self.animate(0)

    # actuaciones de menu
    def my_popup(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def move(self):
        print('video ->', self.url)
        if os.path.isfile(self.url):
            window = WindowCopyTo(self)
            window.title('MOVER ...')
            window.copy = False
            window.file.set(self.url)
            window.path_to_copy.set(os.path.dirname(self.url))
            window.grab_set()

    def copy(self):
        print('video ->', self.url)
        if os.path.isfile(self.url):
            option = {'width': 600, 'height': 120}
            window = WindowCopyTo(self, **option)
            # window.title('MOVER ...')
            # window.copy = False
            window.file.set(self.url)
            window.path_to_copy.set(os.path.dirname(self.url))
            window.grab_set()

    def remove(self):
        """Action remove file or delete"""
        from tkinter.messagebox import askyesno
        print('video ->', self.url)
        if os.path.isfile(self.url):
            answer = askyesno(title='Confirmation',
                              message='Are you sure that you want to remove?')
            if answer:
                ToolFile.remove(self.url)

    def rename(self):
        print('video ->', self.url)
        if os.path.isfile(self.url):
            window = OpenDialogRename(self)
            window.file.set(self.url)
            window.name.set("New-" + os.path.basename(self.url))
            window.grab_set()
            # TODO: al cambiar el nombre, modificar self.url base.

    def check_exist(self)-> tuple:
        '''check if file url video exist an its gif 
            return:
                True if exist url file, True if exist gif file
        '''
        res, ges = False, False
        if os.path.exists(self.url):
            self.pathdir.set(os.path.dirname(self.url)) # dir content video
            self.pathdirthum.set(os.path.join(self.pathdir.get(), '.Thumbails'))
            self.name.set(os.path.basename(self.url))
            self.namethumb.set(self.name.get() + '_nfx_.gif')
            self.source = os.path.join(self.pathdirthum.get(), self.namethumb.get())
            if os.path.exists(self.source):
                ges = True
            res = True
        return res, ges
        
    def animate(self, counter):
        # print(counter)
        self.index = counter
        self.photo = ImageTk.PhotoImage(self.graphics.getImagenSecuencia(self.index))
        self.canvas.itemconfig(self.image, image=self.photo)
        self.count = self.graphics.imgBox.count
        if not self.animating:
            return
        self.after(self.timer, lambda: self.animate((counter+1)% self.count))

    def enter(self, event):
        self.animating = True
        self.animate(self.index)
    
    def leave(self, event):
        self.animating = False

    def double_click_canvas(self, event):
        #obtener el nombre del fichero de video
        print('video ->', self.url)
        if os.path.isfile(self.url):
            thread = Thread(target=self.tarea, args=("ffplay " + "\"" + self.url + "\"",))
            thread.daemon = True
            thread.start()

    @staticmethod
    def tarea(args=None):
        if not args:
            return
        os.system(args)

    def open(self, file=None):
        if not file: return
        if sys.platform == "win32":
            os.startfile(file)
        else:
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, file])


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("400x600")
    app = SpritePane(root, url='Work/Videos/1ec6f7f9bca04bf80cc8a491cf45899c.flv', timer=200)
    app.pack()
    app1 = SpritePane(root, url='Work/Videos/780bea12c379871bc18938bd6592fe17.flv', timer=200)
    app1.pack()
    app2 = SpritePane(root, url='Work/Videos/4bbc5c0df3a2ed8960ad686ecca4cafc.mp4', timer=200)
    app2.pack()
    root.mainloop()
