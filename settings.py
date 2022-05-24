class Settings:

    def __init__(self) -> None:
        """Initialize the game's static settings."""
        # Screen size settings
        self.screen_width = 1200
        self.screen_height = 800
        # Background color
        self.bg_color = (230, 230, 230)
        # Ship speed settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Setting for bullet
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Setting for alien
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 means right; -1 means left.
        self.fleet_direction = 1

        # Improve game speed
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings may change depend on game status"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction 1 means right, -1 means left
        self.fleet_direction = 1

    def increase_speed(self):
        """Improve speed setting"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
