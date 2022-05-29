import os

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """An alien class"""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load alien image from images and set its rect
        self.file_path = os.path.join(os.path.dirname(__file__), 'images/alien.bmp')
        self.image = pygame.image.load(self.file_path)
        self.rect = self.image.get_rect()

        # Start aliens default position to the top right corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's horizon position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Move alien to the up or down"""
        self.y += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.y = self.y

    def check_edges(self):
        """If alien hits the edge, return True"""
        screen_rect = self.screen.get_rect()
        if self.rect.y <= 0 or self.rect.y >= screen_rect.bottom:
            return True
