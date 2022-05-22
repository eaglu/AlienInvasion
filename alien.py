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

    def update(self):
        """Move alien to the right or left"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x


    def check_edges(self):
        """If alien hits the edge, return True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

