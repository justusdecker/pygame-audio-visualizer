
import pygame as pg
from time import perf_counter
from tkinter.filedialog import askopenfilename,asksaveasfilename
import wave
BACKGROUND_COLOR = (36,36,36)

class Animator:
    def __init__(self):
        self.foreground_image = pg.image.load
        self.background_image = pg.image.load
        self.particle_effects = None
        self.particle_animation = None
        self.music = None
        self.destination = None
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
        pass
    def run(self):
        while self.is_running:
            start_time = perf_counter()
            self.window.fill(BACKGROUND_COLOR)
            self.update()
            self.check_events()
            self.delta_time = perf_counter() - start_time
    def update(self):
        pg.display.update()
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                self.is_running = False
                
if __name__ == "__main__":
    App().run()
