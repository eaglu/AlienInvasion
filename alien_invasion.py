import random
import sys

import pygame

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import ScoreBoard
from settings import Settings
from ship import Ship
from star import Star


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((1200, 800))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.bg_color = (230, 230, 230)

        # Create an instance to save game statistics
        # and create a scoreboard
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)

        # Create game characters
        self.ship = Ship(self)
        self.stars = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self._create_stars()

        # Create play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()

            if self.stats.game_active:
                # Update the ship's position
                self.ship.update()
                # update bullets status
                self._update_bullets()
                # update alien status
                self._update_aliens()

            # Redraw the screen during each pass through the loop.
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            self.stats.check_highest_score()
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_play_button(self, mouse_pos):
        """When player clicks the play button, start a new game."""
        if self.play_button.rect.collidepoint(mouse_pos):
            # Reset game settings
            self.settings.initialize_dynamic_settings()
            # Reset game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Clear aliens and bullets remain
            self.aliens.empty()
            self.bullets.empty()

            # Create new aliens and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide mouse point
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Create a new bullet then put it intro bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            bullet = Bullet(self)
            self.bullets.add(bullet)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)

        # Show stars
        self.stars.draw(self.screen)

        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Show score
        self.sb.show_score()

        # If game is inactive, draw the play button
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.right >= self.screen.get_rect().right:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Response to bullet and alien collisions"""
        # Delete bullet and alien
        # Check if bullets hit aliens
        # if so ,delete the bullet and alien
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # Check if  aliens are all destroyed
        # if so, create new group of aliens
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Improve game level
            self.stats.level += 1
            self.sb.prep_level()

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        scr_width, scr_height = pygame.display.get_surface().get_size()
        alien.x = scr_width - (alien_width + 2 * alien_width * alien_number)
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number

        self.aliens.add(alien)

    def _update_aliens(self):
        """Check if any alien hit the edge
        and update aliens' position"""
        self._check_fleet_edges()
        for alien in self.aliens.sprites():
            alien.y = self.settings.alien_speed * self.settings.fleet_direction
            alien.rect.y += alien.y

        # Check if any alien hits the ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check if any alien hits the bottom of the screen
        self._check_aliens_bottom()

    def _create_fleet(self):
        # Create an alien and calculate the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (4 * alien_width)
        number_aliens_x = available_space_x // (4 * alien_width)

        # Calculate the number of rows of aliens that the screen can fit.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create aliens group
        for alien_number in range(number_aliens_x):
            for row_number in range(number_rows):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        """Response when alien hits the edge"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_rect().bottom or alien.rect.top <= 0:
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """Check if aliens get to the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Change the entire aliens and change the aliens' direction."""
        for alien in self.aliens.sprites():
            # alien.rect.x -= self.settings.fleet_drop_speed
            alien.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Response to ship hit by alien"""
        if self.stats.ships_left > 0:
            # Decrease ship's live
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Clear aliens and bullets remain
            self.aliens.empty()
            self.bullets.empty()

            # Create new aliens and center the ship
            self._create_fleet()
            self.ship.center_ship()
        else:
            # Pause
            self.stats.check_highest_score()
            pygame.mouse.set_visible(True)
            self.stats.game_active = False

    def _create_stars(self):
        """Create stars randomly"""

        # Get star size and screen size
        star = Star(self)
        star_width, star_height = star.rect.size
        scr_width, scr_height = self.screen.get_size()

        # Get how many stars can a row or a list contains
        row_number = scr_height // star_height
        list_number = scr_width // star_width

        # Zip their index together and see how many stars to init
        star_number = min(row_number, list_number)
        row_indexes = random.sample(range(0, row_number), star_number)
        list_indexes = random.sample(range(0, list_number), star_number)
        zipped_pos = zip(row_indexes, list_indexes)

        for pos in zipped_pos:
            row_index, list_index = pos
            self._create_star(row_index, list_index)

    def _create_star(self, row_index, list_index):
        """Create a star and place it by row_index and list_index."""
        star = Star(self)
        star_width, star_height = star.rect.size
        star.rect.x = star_width * list_index
        star.rect.y = star_height * row_index

        self.stars.add(star)


if __name__ == "__main__":
    a = AlienInvasion()
    a.run_game()
