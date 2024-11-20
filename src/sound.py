import pygame


class Sound:
    def __init__(self, path):  # path of the sound
        self.path = path
        self.sound = pygame.mixer.Sound(path)
        pass

    def play(self):
        pygame.mixer.Sound.play(self.sound)
