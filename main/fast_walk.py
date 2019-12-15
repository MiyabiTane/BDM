import pygame.mixer
import time

class FastWalk():

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('./sound/tetetete.mp3')

    def play(self):
        pygame.mixer.music.play(1)
        time.sleep(1)
        pygame.mixer.music.stop()
