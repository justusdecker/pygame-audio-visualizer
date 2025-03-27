
import pygame as pg
from time import perf_counter
from tkinter.filedialog import askopenfilename,asksaveasfilename
from os import path
import wave
BACKGROUND_COLOR = (36,36,36)
def get_image(title:str) -> pg.Surface:
    filepath = askopenfilename(title=title,filetypes=[("Images",(".png",".jpeg",".jpg",".webp"))])
    if path.isfile(filepath):
        return pg.image.load(filepath)
    return pg.Surface((1,1),pg.SRCALPHA)

class Animator:
    def __init__(self):
        self.background_image = get_image("Background image")
        self.foreground_image = get_image("Foreground image")
        
        
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
    def show(self,app):
        app.window.blit(self.background_image,self.bi_pos)
        app.window.blit(self.foreground_image,self.fi_pos)
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
    def run(self):
        while self.is_running:
            start_time = perf_counter()
            self.window.fill(BACKGROUND_COLOR)
            self.update()
            self.check_events()
            self.delta_time = perf_counter() - start_time
    def update(self):
        self.animator.show(self)
        pg.display.update()
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                self.is_running = False
                
if __name__ == "__main__":
    App().run()
