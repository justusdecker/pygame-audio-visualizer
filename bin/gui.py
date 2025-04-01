from pygame import Rect
from pygame_gui.elements import UIButton,UITextEntryLine
from pygame_gui import UIManager
class GUI:
    def __init__(self,quarter_screen_width:int,manager:UIManager):
        self.fil = UIButton(Rect(0,0,quarter_screen_width,32),"Foreground Image load",manager)
        self.bil = UIButton(Rect(0,32,quarter_screen_width,32),"Background Image load",manager)
        self.mil = UIButton(Rect(0,64,quarter_screen_width,32),"Music load",manager)
        
        self.output_res_input_w = UITextEntryLine(Rect(0,96,quarter_screen_width//2,32),manager,placeholder_text="width")
        self.output_res_input_h = UITextEntryLine(Rect(quarter_screen_width//2,96,quarter_screen_width//2,32),manager,placeholder_text="height")
        self.output_res_input_w.set_allowed_characters([i for i in"1234567890"])
        self.output_res_input_h.set_allowed_characters([i for i in"1234567890"])
        
        self.pivot_input_x = UITextEntryLine(Rect(0,128,quarter_screen_width//2,32),manager,placeholder_text="pivot x")
        self.pivot_input_y = UITextEntryLine(Rect(quarter_screen_width//2,128,quarter_screen_width//2,32),manager,placeholder_text="pivot y")
        self.pivot_input_x.set_allowed_characters([i for i in"1234567890"])
        self.pivot_input_y.set_allowed_characters([i for i in"1234567890"])
        
        self.pos_input_x = UITextEntryLine(Rect(0,160,quarter_screen_width//2,32),manager,placeholder_text="position x")
        self.pos_input_y = UITextEntryLine(Rect(quarter_screen_width//2,160,quarter_screen_width//2,32),manager,placeholder_text="position y")
        self.pos_input_x.set_allowed_characters([i for i in"1234567890"])
        self.pos_input_y.set_allowed_characters([i for i in"1234567890"])
        
        self.smoothness_input = UITextEntryLine(Rect(0,160,quarter_screen_width//2,32),manager,placeholder_text="smoothness")
        self.resize_val_input = UITextEntryLine(Rect(quarter_screen_width//2,160,quarter_screen_width//2,32),manager,placeholder_text="resize value")
        self.smoothness_input.set_allowed_characters([i for i in"1234567890."])
        self.resize_val_input.set_allowed_characters([i for i in"1234567890."])
        
        self.preview_button = UIButton(Rect(0,192,quarter_screen_width,32),"Preview Video",manager)
        self.render_button = UIButton(Rect(0,224,quarter_screen_width,32),"Render Video",manager)
        self.render_button.disable()