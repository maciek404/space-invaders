import turtle
import tkinter
from turtle import Screen
import time
import random

import theme
from bullet import Bullet
from player import Player, register_player_shape
from alien import Alien, register_alien_shape
from barrier import Barrier, BARRIER_SHAPE_MASK
from scoreboard import Scoreboard
from theme import alien_color_for_row
from starfield import Starfield
from explosion import Explosion

is_bullet_ready = True
BULLET_COOLDOWN = 10
cooldown_counter = 0

ALIEN_ROWS = 5
ALIEN_COLUMNS = 8
ALIEN_START_X = -210
ALIEN_START_Y = 250
ALIEN_COLUMN_SPACING = 60
ALIEN_ROW_SPACING = 40
SCREEN_LEFT_EDGE = -380
SCREEN_RIGHT_EDGE = 380
ALIEN_DIRECTION = 1
ALIEN_BASE_SPEED = 2
ALIEN_SPEED_INCREMENT = 2

ALIEN_HIT_DISTANCE = 15
PLAYER_HIT_DISTANCE = 20
GAME_OVER_LINE_Y = -230

ALIEN_FIRE_INTERVALS = 40
ALIEN_FIRE_CHANCE = 0.5
alien_fire_counter = 0

BARRIER_HIT_DISTANCE = 20
BARRIER_CENTERS_X = [-270, -90, 90, 270]
BARRIER_Y_START = -150
SEGMENT_SPACING = 12

game_is_on = True


def create_barriers():
    rows = len(BARRIER_SHAPE_MASK)
    cols = len(BARRIER_SHAPE_MASK[0])

    for center_x in BARRIER_CENTERS_X:
        for row in range(rows):
            for col in range(cols):
                if not BARRIER_SHAPE_MASK[row][col]:
                    continue

                x = center_x + (col - cols / 2) * SEGMENT_SPACING
                y = BARRIER_Y_START - row * SEGMENT_SPACING
                segment = Barrier(x, y)
                barriers.append(segment)


def create_fleet():
    for row in range(ALIEN_ROWS):
        for col in range(ALIEN_COLUMNS):
            x = ALIEN_START_X + col * ALIEN_COLUMN_SPACING
            y = ALIEN_START_Y - row * ALIEN_ROW_SPACING
            color = alien_color_for_row(row)
            new_alien = Alien(x, y, color)
            aliens.append(new_alien)


def fire_bullet():
    global is_bullet_ready
    if is_bullet_ready:
        new_bullet = Bullet(player.xcor(), player.ycor() + 10, theme.BULLET_COLOR)
        bullets.append(new_bullet)
        is_bullet_ready = False


def alien_fire():
    global alien_fire_counter
    alien_fire_counter += 1
    if alien_fire_counter < ALIEN_FIRE_INTERVALS:
        return
    alien_fire_counter = 0

    if not aliens:
        return
    if random.random() > ALIEN_FIRE_CHANCE:
        return

    shooter = random.choice(aliens)
    new_bullet = Bullet(shooter.xcor(), shooter.ycor(), theme.ALIEN_BULLET_COLOR, heading=270)
    alien_bullets.append(new_bullet)


def check_bullet_barrier_collision():
    for bullet in bullets[:]:
        closest_segment = None
        closest_distance = BARRIER_HIT_DISTANCE

        for segment in barriers[:]:
            distance = bullet.distance(segment)
            if distance < closest_distance:
                closest_distance = distance
                closest_segment = segment

        if closest_segment:
            bullet.hideturtle()
            bullets.remove(bullet)
            closest_segment.hideturtle()
            barriers.remove(closest_segment)


def check_alien_barrier_collision():
    for alien in aliens:
        for segment in barriers[:]:
            if alien.distance(segment) < BARRIER_HIT_DISTANCE:
                segment.hideturtle()
                barriers.remove(segment)


def check_bullet_alien_collision():
    for bullet in bullets[:]:
        for alien in aliens[:]:
            if bullet.distance(alien) < ALIEN_HIT_DISTANCE:
                bullet.hideturtle()
                bullets.remove(bullet)
                explosion_color = alien.fillcolor()
                explosions.append(Explosion(alien.xcor(), alien.ycor(), explosion_color))
                alien.hideturtle()
                aliens.remove(alien)
                scoreboard.increase_score(10)
                break


def check_alien_bullet_player_collision():
    global game_is_on
    for bullet in alien_bullets[:]:
        if bullet.distance(player) < PLAYER_HIT_DISTANCE:
            bullet.hideturtle()
            alien_bullets.remove(bullet)

            explosions.append(Explosion(player.xcor(), player.ycor(), theme.PLAYER_COLOR))
            player.hideturtle()
            scoreboard.lose_life()

            if scoreboard.lives <= 0:
                game_is_on = False
                scoreboard.game_over()
            else:
                player.reset_position()
                player.showturtle()

            break


def check_alien_player_collision():
    global game_is_on
    for alien in aliens:
        if alien.distance(player) < PLAYER_HIT_DISTANCE or alien.ycor() < GAME_OVER_LINE_Y:
            explosions.append(Explosion(player.xcor(), player.ycor(), theme.PLAYER_COLOR))
            player.hideturtle()
            game_is_on = False
            scoreboard.game_over()
            break


def check_level_complete():
    global alien_speed, ALIEN_BASE_SPEED
    if not aliens:
        ALIEN_BASE_SPEED += ALIEN_SPEED_INCREMENT
        scoreboard.next_level()
        create_fleet()


def restart_game():
    global game_is_on, ALIEN_DIRECTION, alien_speed, alien_fire_counter

    if game_is_on:
        return

    for bullet in bullets:
        bullet.hideturtle()
    bullets.clear()

    for bullet in alien_bullets:
        bullet.hideturtle()
    alien_bullets.clear()
    alien_fire_counter = 0

    for alien in aliens:
        alien.hideturtle()
    aliens.clear()

    for segment in barriers:
        segment.hideturtle()
    barriers.clear()

    for explosion in explosions:
        explosion.force_finish()
    explosions.clear()

    player.showturtle()
    player.reset_position()
    scoreboard.reset()

    ALIEN_DIRECTION = 1
    # alien_speed = ALIEN_BASE_SPEED
    ALIEN_BASE_SPEED = 2

    create_fleet()
    create_barriers()

    game_is_on = True


screen = Screen()
screen.setup(width=800, height=600, startx=300, starty=950)
screen.bgcolor(theme.BACKGROUND_COLOR)
screen.title("Space Invaders")
screen.tracer(0)

starfield = Starfield()
register_player_shape(screen)
register_alien_shape(screen)

player = Player()
scoreboard = Scoreboard()

explosions = []
bullets = []
aliens = []
alien_bullets = []
barriers = []

create_barriers()
create_fleet()

screen.listen()
screen.onkey(player.move_left, "Left")
screen.onkey(player.move_right, "Right")
screen.onkey(fire_bullet, "space")
screen.onkey(restart_game, "r")
screen.onkey(restart_game, "R")

try:
    while True:
        time.sleep(0.02)
        screen.update()

        for explosion in explosions[:]:
            explosion.update()
            if explosion.is_finished():
                explosions.remove(explosion)

        if not game_is_on:
            continue

        # --- bullet cooldown ---
        if not is_bullet_ready:
            cooldown_counter += 1
            if cooldown_counter >= BULLET_COOLDOWN:
                is_bullet_ready = True
                cooldown_counter = 0

        # --- bullet movement ---
        for bullet in bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                bullet.hideturtle()
                bullets.remove(bullet)

        # --- alien bullet movement ---
        for bullet in alien_bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                bullet.hideturtle()
                alien_bullets.remove(bullet)

        # --- aliens movement ---
        reached_edge = False
        for alien in aliens:
            alien.move_sideways(ALIEN_DIRECTION, ALIEN_BASE_SPEED)
            if alien.xcor() > SCREEN_RIGHT_EDGE or alien.xcor() < SCREEN_LEFT_EDGE:
                reached_edge = True

        if reached_edge:
            ALIEN_DIRECTION *= -1
            for alien in aliens:
                alien.move_down()
        alien_fire()

        # --- collisions ---
        check_bullet_barrier_collision()
        check_bullet_alien_collision()
        check_alien_bullet_player_collision()
        check_alien_barrier_collision()
        check_alien_player_collision()
        check_level_complete()

except (turtle.Terminator, tkinter.TclError):
    pass
