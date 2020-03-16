#! /usr/bin/env python3
# _*_ coding:UTF-8 _*_
import tkinter as tk
from pil import Image, ImageTk, ImageSequence
import os
from threading import Thread

class SpritePane(tk.Frame):
    def __init__(self, parent, fileImagen=None, timer=None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.fileImagen= fileImagen
        if not fileImagen:
            self.fileImagen = './../work/thumbails/candy.flv_thumbs_0000.gif'
        self.timer = timer
        if not timer:
            self.timer = 850
        self.pathfile = tk.StringVar(value=self.fileImagen)
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open(self.fileImagen))]
        self.img_width = self.sequence[0].width()
        self.img_height = self.sequence[0].height()
        print("w x h : {} x {}".format(self.img_width,self.img_width))
        self.canvas = tk.Canvas(self, width=self.img_width, height=self.img_height, bg="yellow")
        self.canvas.pack()
        self.image = self.canvas.create_image(self.img_width/2, self.img_height/2, image=self.sequence[0])
        self.canvas.bind('<Enter>', self.enter)
        self.canvas.bind('<Leave>', self.leave)
        self.canvas.bind('<Double-Button-1>', self.double_click_canvas)
        self.animating = True
        # self.animate(0)
        self.index = 0

    def animate(self, counter):
        # print(counter)
        self.index = counter
        self.canvas.itemconfig(self.image, image=self.sequence[counter])
        if not self.animating:
            return
        self.after(self.timer, lambda: self.animate((counter+1)% len(self.sequence)))

    def enter(self, event):
        self.animating = True
        self.animate(self.index)
    
    def leave(self, event):
        self.animating = False

    def double_click_canvas(self, event):
        #import os
        print('double-click-canvas: file:->{}'.format(self.pathfile.get()))
        print('basename: -> ', os.path.basename(self.pathfile.get()))
        print('split: -> ', os.path.split(self.pathfile.get()))
        print('dirname: -> ', os.path.dirname(self.pathfile.get()))
        print('directorio activo: -> ', os.getcwd())
        address= [os.getcwd(), 'videos', os.path.basename(self.pathfile.get())]
        print(address)
        #obtener el nombre del fichero de video
        _video_name = os.path.basename(self.pathfile.get()).split("_thumbs_")[0]
        _video = os.path.join(os.path.dirname(self.pathfile.get()), './../',  _video_name)
        print('video ->', _video)
        if os.path.isfile(_video):
            thread = Thread(target=self.tarea, args=("ffplay " + "\"" + _video + "\"",))
            thread.daemon = True
            thread.start()


    @staticmethod
    def tarea(args=None):
        if not args:
            return
        os.system(args)


def main():
    root = tk.Tk()
    root.geometry("400x600")
    app = SpritePane(root) #, fileImagen='./../work/thumbails/cotton.gif', timer=200)
    app.pack()
    app2 = SpritePane(root, fileImagen='./../work/thumbails/Italian.mp4_thumbs_0000.gif')
    app2.pack()
    app3 = SpritePane(root, fileImagen='./../work/thumbails/Mexican.mp4_thumbs_0000.gif')
    app3.pack()
    #app4 = SpritePane(root, fileImagen='./../work/thumbails/catty.gif')
    root.mainloop()


if __name__ == '__main__':
    main()
