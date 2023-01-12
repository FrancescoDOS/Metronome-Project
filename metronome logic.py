from colour import Color as C
import pygame as py
import time as t

import random as rdm
import menu 

print("\033c")

# ====================== Screen Stuff ======================
py.display.set_caption('Metronome Visual.exe')
program_icon = py.image.load("Metronome project\Icons\metronome icon.png")
py.display.set_icon(program_icon)

WIDTH, HIGHT             =  1600, 900
Update_Rate, Framerate   =  60, 240
Running                  =  False
# ===========================================================

# ======================= BPM Control =======================
py.mixer.init(buffer = 2048)
Colision_Sound_Default   = py.mixer.Sound("Metronome project\Sounds\Bubble.mp3")
Colision_Sound_Default.set_volume(0.1)

Beats_Per_Minute_Default = 60
Beats_Per_Second         = Beats_Per_Minute_Default / Update_Rate
Object_Speed_Default     = HIGHT * (Beats_Per_Second / 60)

print (f"BPM : {Beats_Per_Minute_Default}\nBPS : {Beats_Per_Second}\nSpeed : {(HIGHT * (Beats_Per_Second) / 60)} Pixels/Second\n")
# ===========================================================

# ========================= COLORS =========================
EGG_SHELL_WHITE =  235, 235, 245
WHITE           =  255, 255, 255
BLACK           =  0  , 0  , 0
GREY            =  127, 127, 127
ORANGE          =  255, 101, 0  
DARK_BLUE       =  12 , 24 , 36

RED_PERCENT     = C(rgb = (1, 0, 0))
BLUE_PERCENT    = C(rgb = (0, 0, 1))
PURPLE_PERCENT  = C(rgb = (0.627, 0.125, 0.941))
PINK_PERCENT	= C(rgb = (0.89, 0.11, 0.47))
gradient        = []
# ===========================================================

class Circle():
    def __init__(self, color = None, coords = [0 ,0], radius = 20, border_width = 0, colision_sound = Colision_Sound_Default, direction = 1):
        
        self.color          =   color
        self.coords         =  coords
        self.radius         =  radius
        self.border_width   =  border_width
        self.colision_sound = colision_sound 
        self.direction      = direction
    
    def info(self):
        return [self.color, self.coords, self.radius, self.border_width]

def generate_color_gradient(N_Obj):
    global gradient
    gradient = list(RED_PERCENT.range_to(PINK_PERCENT,N_Obj)) 
    for i in range(len(gradient)): # hex to R G B percentages (1 , 1,  1) == white
        gradient[i] = list(gradient[i].rgb)
        for x in range(len(gradient[i])): # percentage of rgb converted to actual R G B values  
            gradient[i][x] = int(int(gradient[i][x] * 100) * 255 / 100)
        gradient[i] = tuple(gradient[i])

def set_settings():
    # Bpm = int(input("Enter a BPM:\n"))
    # Obj_Type = input("Enter what king of object you want:\n(1 : Cube | 2 : Circle)\n>>> ")
    # Objs_Pos = input("Enter where the objects should start from\n(1 : Up | 2 : Down | 3 : Left | 4 : Right)\n>>> ")
    N_Obj = 100 # int(input("Enter the number of objects for this run:\n>>> "))
    Obj_Size = 20 # int(input("Enter how big you want the objects to be:\n>>> "))
    return N_Obj, Obj_Size

def play_colide_sound(obj):
    obj.colision_sound.play()

def calculate_bpm_speed(obj, index):
    return HIGHT * ((Beats_Per_Second / 1.001**index) / 60)

def align_obj(Object_List, Obj_Size, pos = 1):
    obj_size_offset = Obj_Size
    X_obj_offset    = WIDTH / len(Object_List) 
    # Y_obj_offset  = HIGHT / len(Object_List)
    
    if pos == 1: # Up
        for index, obj in enumerate(Object_List):
            obj.coords = [obj.coords[0] + (obj_size_offset + (X_obj_offset * index)), obj.coords[1] + obj_size_offset]
 
    elif pos == 2: # Down
        for index, obj in enumerate(Object_List):
            obj.coords = [obj.coords[0] + (obj_size_offset + (X_obj_offset * index)), obj.coords[1] + HIGHT - obj_size_offset]

    elif pos == 3: # Mixed (Up & down)
        switch = 0
        for index, obj in enumerate(Object_List):
            if switch == 0:
                obj.coords = [obj.coords[0] + (obj_size_offset + (X_obj_offset * index)), obj.coords[1] + obj_size_offset]
                switch = 1
            elif switch == 1:
                obj.coords = [obj.coords[0] + (obj_size_offset + (X_obj_offset * index)), obj.coords[1] + HIGHT - obj_size_offset]
                switch = 0      

def update_object_position(Object_List, dt):
    

    for index, obj in enumerate(Object_List):
        if obj.direction == 1:
            obj.coords = [obj.coords[0], obj.coords[1] + calculate_bpm_speed(obj, index) * dt]
            
            if obj.coords[1] + obj.radius >= HIGHT:
                obj.coords = [obj.coords[0], HIGHT - obj.radius]
                obj.direction = -1
                play_colide_sound(obj)
        
        elif obj.direction == -1:
            obj.coords = [obj.coords[0], obj.coords[1] - calculate_bpm_speed(obj, index) * dt]
            
            if obj.coords[1] - obj.radius <= 0:
                obj.coords = [obj.coords[0], 0 + obj.radius]
                obj.direction = 1
                play_colide_sound(obj)

def update_screen_content(Object_List, window):
    
    window.fill(BLACK)
    
    for index, obj in enumerate(Object_List):
        try:
            py.draw.line(window, obj.color, obj.coords, Object_List[index + 1].coords, 3)
        except IndexError:
            break

    for obj in Object_List:
        py.draw.circle(window, *obj.info())
        py.draw.circle(window, WHITE, obj.coords, obj.radius, 3)

def main():
    
    

    # ========================== Var Init Stuff ========================== 
    Running         = True
    window          = py.display.set_mode((WIDTH,HIGHT), py.RESIZABLE, 32)
    Main_Clock      = py.time.Clock()
    Old_time        = t.time()

    N_Obj, Obj_Size = set_settings()
    Object_List     = [Circle(None, [0, 0], Obj_Size) for _ in range(N_Obj)]
    
    align_obj(Object_List, Obj_Size, 3)
    generate_color_gradient(N_Obj)

    for index, obj in enumerate(Object_List):
        obj.color = gradient[index]
    # ====================================================================

    # menu.main(window)

    while Running:
        # ===== Non Framerate Dependant Movement =====
        dt       = t.time() - Old_time
        dt      *= Update_Rate
        Old_time = t.time()
        # ============================================

        for event in py.event.get():
            if event.type == py.QUIT:
                Running = False 
                break

        update_object_position(Object_List, dt)
        update_screen_content(Object_List, window)
        
        py.display.flip()
        Main_Clock.tick(Framerate)

if __name__ == "__main__":
    main()