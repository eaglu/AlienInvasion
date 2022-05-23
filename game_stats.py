class GameStats:
    """Tack game statistics"""

    def __init__(self,ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics may change during the game running"""
        self.ships_left = self.settings.ship_limit