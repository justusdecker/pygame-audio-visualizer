"""
(c) 2025 - The PAV Project by Justus Decker
Documentation is coming soon!
"""
from bin.ext import *

class App:
    delta_time = 0
    clock = pg.Clock()
    width = 1280
    height = 720
    window = pg.display.set_mode((width,height))
    main_surface = pg.Surface((width*2,height*2))
    manager = pgg.UIManager((width,height),)
    playing = False
    is_running = True
    quarter_screen_width = int(width * .25)
    ui_elements = GUI(quarter_screen_width,manager)
    resize = .03
    def __init__(self):
        self.animator = Animator(self)

        
    def run(self):
        while self.is_running:
            start_time = perf_counter()
            self.main_surface.fill(BACKGROUND_COLOR)
            self.update()
            self.check_events()
            pg.display.update()
            self.delta_time = perf_counter() - start_time
        pg.quit()  
    def update(self):
        if self.playing:
            self.animator.smooth_resize(self.resize,self.delta_time,self.audio.frames)
            self.animator.show()
        
    def check_events(self):
        
        for event in pg.event.get():
            self.manager.process_events(event)
            if event.type == pg.QUIT:
                self.is_running = False
            if event.type == pgg.UI_BUTTON_PRESSED:
                if event.ui_element == self.ui_elements.bil:
                    self.animator.background_image = get_image("Background image")
                if event.ui_element == self.ui_elements.fil:
                    self.animator.foreground_image = get_image("Foreground image")
                if event.ui_element == self.ui_elements.mil:
                    self.animator.music = get_music("BGM")
                if event.ui_element == self.ui_elements.preview_button:
                    if pg.mixer.music.get_busy():
                        pg.mixer.music.stop()
                        self.playing = False
                        continue
                    if self.animator.music is not None and self.animator.foreground_image is not None \
                        and self.animator.background_image is not None:
                        self.animator.set_values()
                        resize, smoothness = get_str2float(self.ui_elements.resize_val_input.text,.125),get_str2float(self.ui_elements.smoothness_input.text,15)
                        freqs = get_str2float(self.ui_elements.frq_min.text,0),get_str2float(self.ui_elements.frq_max.text,440)
                        self.animator.offset = [get_str2int(self.ui_elements.pos_input_x.text,0),get_str2int(self.ui_elements.pos_input_y.text,0)]
                        print(resize)
                        self.audio = Audio(
                            frequencys=freqs,
                            resize_value=resize,
                            smoothness=smoothness,
                            filename=self.animator.music
                            )
                        self.audio.open()
                        self.audio.frames = []
                        self.audio.get_audio()
                        self.playing = True
                        pg.mixer.init()
                        pg.mixer.music.load(self.animator.music)
                        pg.mixer.music.play()

                        
        self.manager.update(self.delta_time)
        self.manager.draw_ui(self.window)
                
if __name__ == "__main__":
    App().run()
