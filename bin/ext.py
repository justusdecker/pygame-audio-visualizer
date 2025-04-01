import pygame as pg
from time import perf_counter
from tkinter.filedialog import askopenfilename,asksaveasfilename
from os import path
import wave
from numpy.fft import fft
from numpy import frombuffer,int16
from math import sqrt
from subprocess import run, CREATE_NO_WINDOW
from json import load,dumps
import pygame_gui as pgg
from bin.gui import GUI
from bin.animator import Animator
pg.init()

def get_music(title:str) -> str:
    filepath = askopenfilename(title=title,filetypes=[("Music",(".mp3",".wav"))])
    if path.isfile(filepath):
        return filepath
    return ""

def get_image(title:str) -> pg.Surface:
    filepath = askopenfilename(title=title,filetypes=[("Images",(".png",".jpeg",".jpg",".webp"))])
    if path.isfile(filepath):
        return pg.image.load(filepath)
    return pg.Surface((1,1),pg.SRCALPHA)

BACKGROUND_COLOR = (36,36,36)