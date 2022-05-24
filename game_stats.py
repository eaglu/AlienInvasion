class GameStats:
    """Tack game statistics"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        # Start game in inactive state
        self.game_active = False
        # High score should not be reset in any situation
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics may change during the game running"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
