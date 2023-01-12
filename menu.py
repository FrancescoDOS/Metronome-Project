import pygame as py
import time as t

Update_Rate, Framerate   =  60, 240
Running = False
Font = "Metronome project\Fonts\Helvetica Rounded LT Bold.ttf"

EGG_SHELL_WHITE =  235, 235, 245
WHITE           =  255, 255, 255
BLACK           =  0  , 0  , 0
GREY            =  127, 127, 127
ORANGE          =  255, 101, 0  
DARK_BLUE       =  12 , 24 , 36

Main_Menu = [
    "Main Menu",
    "Start",
    "Settings"
]


# def draw_text(window, text):
#     text_surface = py.font.Font(Font,20).render(text, True, WHITE)
#     text_rect = text_surface.get_rect()
#     text_rect.center = ()
#     window.blit(text_surface,text_rect)


def main(window):

    Main_Clock = py.time.Clock()
    Old_time   = t.time()
    Running    = True
    
    while Running:
        dt       = t.time() - Old_time
        dt      *= Update_Rate
        Old_time = t.time()
        
        for event in py.event.get():
            if event.type == py.QUIT:
                Running = False 
                break
        
        window.fill(DARK_BLUE)

        py.display.flip()
        Main_Clock.tick(Framerate)
