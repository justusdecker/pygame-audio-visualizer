"""
(c) 2025 - The PAV Project by Justus Decker
Documentation is coming soon!
"""
from bin.ext import *


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
        self.sF = wave.open(self.filename,'rb')
        self.chz = int(self.sF.getframerate()*.01666)
        self.load()
        
    def load(self):
        if self.filename.endswith(".mp3"):
            f = self.filename.split(".mp3")[0]
        if self.filename.endswith(".wav"):
            f = self.filename.split(".wav")[0]
        if path.isfile(f + ".pav"):
            with open(f + ".pav","r") as f_in:
                self.frames = load(f_in)
        else:
            self.frames = []
    def save(self):
        if self.filename.endswith(".mp3"):
            f = self.filename.split(".mp3")[0]
        if self.filename.endswith(".wav"):
            f = self.filename.split(".wav")[0]
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
    
class Animator:
    def __init__(self,app):
        self.app = app
        self.background_image = get_image("Background image")
        self.foreground_image = get_image("Foreground image")
        
        self.fi_manipulated = self.foreground_image.copy()
        self.bi_manipulated = self.background_image.copy()
        
        self.bi_scale = 1.
        self.fi_scale = 1.
        
        self.fi_pos = [(self.app.width//2)-(self.foreground_image.get_width()//2),(self.app.height//2)-(self.foreground_image.get_height()//2)]
        self.bi_pos = [0,0]
        
        self.bi_rot = 0
        self.fi_rot = 0
        
        self.fi_pivot = self.fi_pos.copy()
        self.bi_pivot = self.bi_pos.copy()
        
        self.particle_effects = None
        self.particle_animation = None
        self.music = get_music("BGM")
        self.destination = None
    def smooth_resize(self,value: float):
        self.fi_scale = value
        self.fi_manipulated = pg.transform.scale_by(self.foreground_image,self.fi_scale)
        self.fi_pos = [
            (self.app.width//2)-(self.fi_manipulated.get_width()//2),
            (self.app.height//2)-(self.fi_manipulated.get_height()//2)
            ]
    def show(self):
        self.app.main_surface.blit(self.bi_manipulated,self.bi_pos)
        self.app.main_surface.blit(self.fi_manipulated,self.fi_pos)
        self.app.window.blit(self.app.main_surface,(0,0))

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
    
    fil = pgg.elements.UIButton(pg.Rect(0,0,quarter_screen_width,32),"Foreground Image load",manager)
    bil = pgg.elements.UIButton(pg.Rect(0,0,quarter_screen_width,32),"Background Image load",manager)
    mil = pgg.elements.UIButton(pg.Rect(0,0,quarter_screen_width,32),"Music load",manager)
    
    
    
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
        pos = int(((self.audio_pos) / (len(self.audio.frames)*.0166)) * len(self.audio.frames))
        
        if pos >= len(self.audio.frames): self.is_running = False ; return

        self.animator.smooth_resize(self.audio.frames[pos] *.03)
        self.audio_pos += self.delta_time
        self.animator.show()
        
    def check_events(self):
        
        for event in pg.event.get():
            self.manager.process_events(event)
            if event.type == pg.QUIT:
                self.is_running = False
        self.manager.update(self.delta_time)
        self.manager.draw_ui(self.window)
                
if __name__ == "__main__":
    App().run()
