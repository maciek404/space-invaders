import time
import random
import turtle
import tkinter as tk

import theme
from player import Player
from alien import Alien
from bullet import Bullet
from barrier import Barrier, BARRIER_SHAPE_MASK
from scoreboard import Scoreboard
from starfield import Starfield
from explosion import Explosion

FRAME_DELAY = 0.02

ALIEN_ROWS = 5
ALIEN_COLUMNS = 8
ALIEN_START_X = -210
ALIEN_START_Y = 250
ALIEN_COLUMN_SPACING = 60
ALIEN_ROW_SPACING = 40

SCREEN_LEFT_EDGE = -380
SCREEN_RIGHT_EDGE = 380

ALIEN_HIT_DISTANCE = 15
PLAYER_HIT_DISTANCE = 20

BARRIER_HIT_DISTANCE = 20
BARRIER_CENTER_X = [-270, -90, 90, 270]
BARRIER_Y_START = -150
SEGMENT_SPACING = 12

ALIEN_BASE_SPEED = 5
ALIEN_SPEED_INCREMENT = 1

ALIEN_FIRE_INTERVAL = 40
ALIEN_FIRE_CHANCE = 0.5

BULLET_COOLDOWN = 10


class Game:
    def __init__(self, screen):
        self.screen = screen

        self.starfield = Starfield()
        self.player = Player()
        self.scoreboard = Scoreboard()

        self.game_over_line_y = self.player.ycor() + 30

        self.aliens = []
        self.barriers = []
        self.bullets = []
        self.alien_bullets = []
        self.explosions = []

        self.alien_direction = 1
        self.alien_speed = ALIEN_BASE_SPEED
        self.is_bullet_ready = True
        self.cooldown_counter = 0
        self.alien_fire_counter = 0
        self.game_is_on = True

        self.create_fleet()
        self.create_barriers()
        self._setup_controls()

    # --- Setup ---

    def _setup_controls(self):
        self.screen.listen()
        self.screen.onkey(self.player.move_left, "Left")
        self.screen.onkey(self.player.move_right, "Right")
        self.screen.onkey(self.fire_bullet, "space")
        self.screen.onkey(self.restart_game, "r")
        self.screen.onkey(self.restart_game, "R")

    # --- Create entity ---

    def create_fleet(self):
        for row in range(ALIEN_ROWS):
            for col in range(ALIEN_COLUMNS):
                x = ALIEN_START_X + col * ALIEN_COLUMN_SPACING
                y = ALIEN_START_Y - row * ALIEN_ROW_SPACING
                color = theme.alien_color_for_row(row)
                self.aliens.append(Alien(x, y, color))

    def create_barriers(self):
        rows = len(BARRIER_SHAPE_MASK)
        cols = len(BARRIER_SHAPE_MASK[0])

        for center_x in BARRIER_CENTER_X:
            for row in range(rows):
                for col in range(cols):
                    if not BARRIER_SHAPE_MASK[row][col]:
                        continue
                    x = center_x + (col - cols / 2) * SEGMENT_SPACING
                    y = BARRIER_Y_START - row * SEGMENT_SPACING
                    self.barriers.append(Barrier(x, y))

    # --- Shooting ---

    def fire_bullet(self):
        if self.is_bullet_ready:
            new_bullet = Bullet(self.player.xcor(), self.player.ycor() + 10, theme.BULLET_COLOR)
            self.bullets.append(new_bullet)
            self.is_bullet_ready = False

    def alien_fire(self):
        self.alien_fire_counter += 1
        if self.alien_fire_counter < ALIEN_FIRE_INTERVAL:
            return
        self.alien_fire_counter = 0

        if not self.aliens:
            return
        if random.random() > ALIEN_FIRE_CHANCE:
            return

        shooter = random.choice(self.aliens)
        new_bullet = Bullet(shooter.xcor(), shooter.ycor() - 10, theme.ALIEN_BULLET_COLOR, heading=270)
        self.alien_bullets.append(new_bullet)

    # --- Collisions ---

    def check_bullet_barrier_collision(self):
        for bullet in self.bullets[:]:
            closest_segment = None
            closest_distance = BARRIER_HIT_DISTANCE

            for segment in self.barriers[:]:
                distance = bullet.distance(segment)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_segment = segment

            if closest_segment:
                bullet.hideturtle()
                self.bullets.remove(bullet)
                closest_segment.hideturtle()
                self.barriers.remove(closest_segment)

    def check_bullet_alien_collision(self):
        for bullet in self.bullets[:]:
            for alien in self.aliens[:]:
                if bullet.distance(alien) < ALIEN_HIT_DISTANCE:
                    bullet.hideturtle()
                    self.bullets.remove(bullet)

                    explosion_color = alien.fillcolor()
                    self.explosions.append(Explosion(alien.xcor(), alien.ycor(), explosion_color))

                    alien.hideturtle()
                    self.aliens.remove(alien)
                    self.scoreboard.increase_score(10)
                    break

    def check_alien_player_collision(self):
        for alien in self.aliens:
            if alien.distance(self.player) < PLAYER_HIT_DISTANCE or alien.ycor() < self.game_over_line_y:
                self.explosions.append(Explosion(self.player.xcor(), self.player.ycor(), theme.PLAYER_COLOR))
                self.player.hideturtle()
                self.game_is_on = False
                self.scoreboard.game_over()
                break

    def check_alien_bullet_player_collision(self):
        for bullet in self.alien_bullets[:]:
            if bullet.distance(self.player) < PLAYER_HIT_DISTANCE:
                bullet.hideturtle()
                self.alien_bullets.remove(bullet)

                self.explosions.append(Explosion(self.player.xcor(), self.player.ycor(), theme.PLAYER_COLOR))
                self.player.hideturtle()
                self.scoreboard.lose_life()

                if self.scoreboard.lives <= 0:
                    self.game_is_on = False
                    self.scoreboard.game_over()
                else:
                    self.player.reset_position()
                    self.player.showturtle()
                break

    def check_alien_barrier_collision(self):
        for alien in self.aliens:
            for segment in self.barriers[:]:
                if alien.distance(segment) < BARRIER_HIT_DISTANCE:
                    segment.hideturtle()
                    self.barriers.remove(segment)

    def check_level_complete(self):
        if not self.aliens:
            self.alien_speed += ALIEN_SPEED_INCREMENT
            self.scoreboard.next_level()
            self.create_fleet()

    # --- Restart ---

    def restart_game(self):
        if self.game_is_on:
            return

        for bullet in self.bullets:
            bullet.hideturtle()
        self.bullets.clear()

        for bullet in self.alien_bullets:
            bullet.hideturtle()
        self.alien_bullets.clear()

        for alien in self.aliens:
            alien.hideturtle()
        self.aliens.clear()

        for segment in self.barriers:
            segment.hideturtle()
        self.barriers.clear()

        for explosion in self.explosions:
            explosion.hideturtle()
        self.explosions.clear()

        self.player.showturtle()
        self.player.reset_position()
        self.scoreboard.reset()

        self.alien_direction = 1
        self.alien_speed = ALIEN_BASE_SPEED
        self.alien_fire_counter = 0

        self.create_fleet()
        self.create_barriers()

        self.game_is_on = True

    # --- Frame loop ---

    def _update_bullet_cooldown(self):
        if not self.is_bullet_ready:
            self.cooldown_counter += 1
            if self.cooldown_counter >= BULLET_COOLDOWN:
                self.is_bullet_ready = True
                self.cooldown_counter = 0

    def _update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                bullet.hideturtle()
                self.bullets.remove(bullet)

        for bullet in self.alien_bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                bullet.hideturtle()
                self.alien_bullets.remove(bullet)

    def _update_fleet_movement(self):
        reached_edge = False
        for alien in self.aliens:
            alien.move_sideways(self.alien_direction, self.alien_speed)
            if alien.xcor() > SCREEN_RIGHT_EDGE or alien.xcor() < SCREEN_LEFT_EDGE:
                reached_edge = True

        if reached_edge:
            self.alien_direction *= -1
            for alien in self.aliens:
                alien.move_down()

    def _update_explosions(self):
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.is_finished():
                self.explosions.remove(explosion)

    def _play_frame(self):
        self._update_bullet_cooldown()
        self._update_bullets()
        self._update_fleet_movement()
        self.alien_fire()

        self.check_bullet_barrier_collision()
        self.check_bullet_alien_collision()
        self.check_alien_player_collision()
        self.check_alien_bullet_player_collision()
        self.check_alien_barrier_collision()
        self.check_level_complete()

    def run(self):
        try:
            while True:
                time.sleep(FRAME_DELAY)
                self.screen.update()

                self._update_explosions()

                if not self.game_is_on:
                    continue

                self._play_frame()

        except (turtle.Terminator, tk.TclError):
            pass