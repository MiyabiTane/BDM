import pygame.mixer
import time

class SlowWalk():

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('./sound/zun.mp3')

    def play(self):
        pygame.mixer.music.play(1)
        time.sleep(1)
        pygame.mixer.music.stop()
