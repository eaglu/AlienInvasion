import math

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Manage bullets from ship"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set to correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_height, self.settings.bullet_width)
        self.rect.midright = ai_game.ship.rect.midright
        # Store the bullet's position as a decimal value
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet up the screen"""
        # Update the decimal position of the bullet
        self.x += self.settings.bullet_speed
        # Update the rect position
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
