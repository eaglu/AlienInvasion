import json
import os


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
        self.file_path = os.path.join(os.path.dirname(__file__), 'userdata/score.json')
        self.highest_score = self.get_highest_score()

    def reset_stats(self):
        """Initialize statistics may change during the game running"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def get_highest_score(self):
        """Get the highest score from the json file"""
        high_score = 0
        with open(self.file_path, 'w+') as f:
            if f.readline() == '':
                json.dump({"highest_score": 0}, f)
            else:
                high_score = json.load(f)['highest_score']
        return high_score

    def check_highest_score(self):
        """Check if the current high score is higher than the highest score"""
        if self.highest_score < self.score:
            with open(self.file_path, 'w') as f:
                json.dump({"highest_score": self.score}, f)
