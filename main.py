"""
(c) 2025 - The PAV Project by Justus Decker
Documentation is coming soon!
"""
from bin.ext import *

"""
after preview press:
    -Music play
    -update fg and bg after 
"""

class Audio:
    def __init__(self,
                 frequencys: tuple[int,int] = (0,440),
                 resize_value: float = .125,
                 smoothness: int = 15,
                 filename:str="",):
        self.frequencys = frequencys
        self.resize_value = resize_value
        self.audio_smoothness = smoothness
        self.filename = filename
        self.open()
        self.load()
    def open(self):
        if self.filename is None: self.filename = ""
        if self.filename:
            self.sF = wave.open(self.filename,'rb')
            self.chz = int(self.sF.getframerate()*.01666)
    def get_end(self):
        return self.filename[-4:]
    def get_path_wo_ext(self):

        return self.filename.split(self.get_end())[0]
    def load(self):
        f = self.get_path_wo_ext()
        if path.isfile(f + ".pav"):
            with open(f + ".pav","r") as f_in:
                self.frames = load(f_in)
        else:
            self.frames = []
    def save(self):
        f = self.get_path_wo_ext()
        with open(f + ".pav","w") as f_out:
            f_out.write(dumps(self.frames))
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
            
    def smooth_audio(self):
        for idx in range(0,len(self.frames) - 1):
            self.frames[idx] = sum(self.frames[idx:idx+self.audio_smoothness]) * self.resize_value

    def get_audio(self):

        if not self.frames:
            self.convert()

            self.frames = [sum([sqrt(v.real * v.real + v.imag * v.imag) for v in fft(frombuffer(buff,int16)[self.frequencys[0] if self.frequencys[0] < self.chz else 0:self.frequencys[1] if self.frequencys[1] < self.chz else 440], n=self.chz)]) for buff in [self.sF.readframes(self.chz) for i in range(self.sF.getnframes()//(self.chz))]]

            m = max(self.frames)
            self.frames = [(int(buff) if buff != 0 else 0.00000000001) / m for buff in self.frames.copy()]
            self.smooth_audio()
            self.save()
        self.sF.close()
        return self.frames


class App:
    delta_time = 0
    clock = pg.Clock()
    width = 1280
    height = 720
    window = pg.display.set_mode((width,height))
    main_surface = pg.Surface((width*2,height*2))
    manager = pgg.UIManager((width,height),)

    is_running = True
    quarter_screen_width = int(width * .25)
    ui_elements = GUI(quarter_screen_width,manager)

    def __init__(self):
        self.animator = Animator(self)
        self.audio = Audio(filename=self.animator.music)
        self.audio.get_audio()
    def run(self):
        self.audio_pos = 0
        if self.animator.music:
            pg.mixer.init()
            pg.mixer.music.load(self.animator.music)
            pg.mixer.music.play()
        while self.is_running:
            start_time = perf_counter()
            self.main_surface.fill(BACKGROUND_COLOR)
            self.update()
            self.check_events()
            pg.display.update()
            self.delta_time = perf_counter() - start_time
        pg.quit()  
    def update(self):
        self.animator.smooth_resize(.03,self.delta_time,self.audio.frames)
        self.audio_pos += self.delta_time
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
                    self.animator.music = get_image("BGM")
                    self.audio = Audio()
        self.manager.update(self.delta_time)
        self.manager.draw_ui(self.window)
                
if __name__ == "__main__":
    App().run()
