"""
(c) 2025 - The PAV Project by Justus Decker
Documentation is coming soon!
"""
import pygame as pg
from time import perf_counter
from tkinter.filedialog import askopenfilename,asksaveasfilename
from os import path
import wave
from numpy.fft import fft
from numpy import frombuffer,int16,nan
from math import sqrt
from subprocess import run, CREATE_NO_WINDOW
from threading import Thread

"""
Coming soon:
0.5: 
    keybinds for [pivot, move, rotate, scale...]
0.6:
    add shake effect in bi
0.7:
    Write a particle system.
    Particle system is affected by music peak.
0.8:
    Render video via: moviepy
0.9:
    maybe some fx stuff like: blur

"""

BACKGROUND_COLOR = (36,36,36)
def get_image(title:str) -> pg.Surface:
    filepath = askopenfilename(title=title,filetypes=[("Images",(".png",".jpeg",".jpg",".webp"))])
    if path.isfile(filepath):
        return pg.image.load(filepath)
    return pg.Surface((1,1),pg.SRCALPHA)

class Audio:
    def __init__(self,
                 chunk:int=1024,
                 rate:int=192000,
                 channel:int=1,
                 filename:str="",):
        self.filename = filename
        self.chunk = chunk
        self.rate = rate
        self.channel = channel
        self.frames = []
    def convert(self):
        if not self.filename.endswith(".wav"):
            run(
                [
                    'ffmpeg',
                    '-n',
                    '-i',
                    self.filename,
                    self.filename.split(".")[0] + ".wav"
                    ],
                    CREATE_NO_WINDOW,
                    shell= True
                )
            self.filename = self.filename.split(".")[0] + ".wav"
    def get_audio(self):
        
        if not self.frames:
            self.convert()
            sF = wave.open(self.filename,'rb')
            frames = [sF.readframes(self.chunk) for i in range(sF.getnframes()//(self.chunk//60))]
            for buff in frames:
                fft_complex = fft(frombuffer(buff,int16), n=self.chunk//60)
                s = 0
                #scale_value = self.scale_value * sqrt(max(v.real * v.real + v.imag * v.imag for v in fft_complex))
                for v in fft_complex:s += sqrt(v.real * v.real + v.imag * v.imag)
                self.frames.append(s)
            m = max(self.frames)
            print(self.frames)
            self.frames = [(int(buff) if buff != 0 else 0.00000000001) / m for buff in self.frames.copy()]
            print(self.frames)
                
        return self.frames
    

class Animator:
    def __init__(self):
        self.background_image = get_image("Background image")
        self.foreground_image = get_image("Foreground image")
        
        self.fi_manipulated = self.foreground_image.copy()
        self.bi_manipulated = self.background_image.copy()
        
        self.bi_scale = 1.
        self.fi_scale = 1.
        
        self.fi_pos = [640-(self.foreground_image.get_width()//2),360-(self.foreground_image.get_height()//2)]
        self.bi_pos = [0,0]
        
        self.bi_rot = 0
        self.fi_rot = 0
        
        self.fi_pivot = self.fi_pos.copy()
        self.bi_pivot = self.bi_pos.copy()
        
        self.particle_effects = None
        self.particle_animation = None
        self.music = None
        self.destination = None
    def smooth_resize(self,value: float):
        """
        !Smooth out sizes before rendering
        """

        self.fi_scale = value
        
        self.fi_manipulated = pg.transform.scale_by(self.foreground_image,self.fi_scale)
        self.fi_pos = [640-(self.fi_manipulated.get_width()//2),360-(self.fi_manipulated.get_height()//2)]
    def show(self,app):
        app.window.blit(self.bi_manipulated,self.bi_pos)
        app.window.blit(self.fi_manipulated,self.fi_pos)
    def render(self):
        pass

class App:
    delta_time = 0
    clock = pg.Clock()
    width = 1280
    height = 720
    window = pg.display.set_mode((width,height))
    is_running = True
    def __init__(self):
        self.animator = Animator()
        self.audio = Audio(filename="E:\\musik\\sortiert\\Gamer_Musik\\Battlefield - Wenn nichts geht Song by Execute.mp3")
        self.audio.get_audio()
    def run(self):
        self.audio_pos = 0
        while self.is_running:
            start_time = perf_counter()
            self.window.fill(BACKGROUND_COLOR)
            self.update()
            self.check_events()
            self.delta_time = perf_counter() - start_time
            
    def update(self):
        self.animator.smooth_resize(self.audio.frames[int(self.audio_pos*60)])
        
        self.audio_pos += self.delta_time
        
        self.animator.show(self)
        pg.display.update()
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                self.is_running = False
                
if __name__ == "__main__":
    App().run()
