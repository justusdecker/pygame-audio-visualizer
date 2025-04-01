from pygame import transform

    
class Animator:
    def __init__(self,app):
        self.app = app
        self.background_image = None
        self.foreground_image = None
        self.music = None
        #Diese Elemente werden vom user geladen aber erst nach button press!
        self.offset = [0,0]
       
    def set_values(self):
        self.audio_pos = 0
        self.fi_manipulated = self.foreground_image.copy()
        self.bi_manipulated = self.background_image.copy()
        
        self.bi_scale = 1.
        self.fi_scale = 1.
        
        self.fi_pos = [(self.app.width//2)-(self.foreground_image.get_width()//2)+self.offset[0],(self.app.height//2)-(self.foreground_image.get_height()//2)+self.offset[1]]
        self.bi_pos = [0,0]
        
        self.bi_rot = 0
        self.fi_rot = 0
        
        self.fi_pivot = self.fi_pos.copy()
        self.bi_pivot = self.bi_pos.copy()
        
        self.particle_effects = None
        self.particle_animation = None
        
        self.destination = None
    def smooth_resize(self,scale: float,dt:float,frames:list[float]):
        print(self.offset)
        pos = int(((self.audio_pos) / (len(frames)*.0166)) * len(frames))
        
        if pos >= len(frames): return
        
        self.fi_scale = frames[pos] * scale
        self.fi_manipulated = transform.scale_by(self.foreground_image,self.fi_scale)
        self.fi_pos = [
            (self.app.width//2)-(self.fi_manipulated.get_width()//2)+self.offset[0],
            (self.app.height//2)-(self.fi_manipulated.get_height()//2)+self.offset[1]
            ]
        self.audio_pos += dt
    def show(self):
        self.app.main_surface.blit(self.bi_manipulated,self.bi_pos)
        self.app.main_surface.blit(self.fi_manipulated,self.fi_pos)
        self.app.window.blit(self.app.main_surface,(0,0))
