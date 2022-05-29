import unittest
from unittest.mock import patch

import pygame
from pygame.event import Event

import alien_invasion


class MoveTest(unittest.TestCase):

    def move_up(self: alien_invasion.AlienInvasion):
        """Mock AlienInvasion._check_events() to move ship up by events."""
        scr_height = self.settings.screen_height
        events = [Event(pygame.KEYDOWN, key=pygame.K_UP)] * scr_height
        for event in events:
            self._check_keydown_events(event)
            self.ship.update()

    @patch.object(alien_invasion.AlienInvasion, '_check_events', move_up)
    def test_move_up(self):
        """Test if ship moves up to the top and stopped."""
        ai = alien_invasion.AlienInvasion()
        ai.stats.game_active = True
        ai._check_events()
        assert ai.ship.rect.y == 0

    def move_down(self: alien_invasion.AlienInvasion):
        """Mock AlienInvasion._check_events() to move ship down by events."""
        scr_height = self.settings.screen_height
        events = [Event(pygame.KEYDOWN, key=pygame.K_DOWN)] * scr_height
        for event in events:
            self._check_keydown_events(event)
            self.ship.update()

    @patch.object(alien_invasion.AlienInvasion, '_check_events', move_down)
    def test_move_down(self):
        """Test if ship moves down to the bottom and stopped."""
        ai_game = alien_invasion.AlienInvasion()
        ai_game.stats.game_active = True
        ai_game._check_events()
        assert ai_game.ship.rect.y == ai_game.settings.screen_height - ai_game.ship.rect.height

    def fire(self: alien_invasion.AlienInvasion):
        """Mock AlienInvasion._check_events() to fire by events."""
        events = [Event(pygame.KEYDOWN, key=pygame.K_SPACE)] * 10
        for event in events:
            self._check_keydown_events(event)

    @patch.object(alien_invasion.AlienInvasion, '_check_events', fire)
    def test_fire(self):
        """Test if bullets number got limited."""
        ai_game = alien_invasion.AlienInvasion()
        ai_game.stats.game_active = True
        ai_game._check_events()
        assert len(ai_game.bullets) == 3


if __name__ == '__main__':
    unittest.main()
