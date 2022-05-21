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
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start aliens default position to the top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's horizon position
        self.x = float(self.rect.x)
