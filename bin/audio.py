from wave import open as wav_open
from os import path
from json import load,dumps
from subprocess import run,CREATE_NO_WINDOW
from numpy.fft import fft
from numpy import frombuffer,int16
from math import sqrt
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
            self.sF = wav_open(self.filename,'rb')
            self.chz = int(self.sF.getframerate()*.01666)
    def get_end(self):
        return self.filename[-4:]
    def get_path_wo_ext(self):
        print(self.get_end(),self.filename)
        end = self.get_end()
        print(self.filename.split(end)[0])
        return self.filename.split(end)[0] if end else ""
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
