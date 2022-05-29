import unittest

from alien_invasion import AlienInvasion


class ShipTest(unittest.TestCase):

    def test_ship_hit(self):
        """Test if ship got hit by three times will game restart"""
        ai_game = AlienInvasion()
        for i in range(3):
            ai_game._ship_hit()
        assert ai_game.stats.ships_left == 0
        assert ai_game.stats.game_active is False


if __name__ == '__main__':
    unittest.main()
