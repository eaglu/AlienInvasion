import os

import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load alien image from images and set its rect
        self.file_path = os.path.join(os.path.dirname(__file__), 'images/star.bmp')
        self.image = pygame.image.load(self.file_path)
        self.rect = self.image.get_rect()

        # Start each new star at the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the stars exact horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
