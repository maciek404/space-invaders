import turtle
import tkinter
from turtle import Screen
import time

from bullet import Bullet
from player import Player
from alien import Alien
from barrier import Barrier
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=800, height=600, startx=300, starty=950)
screen.bgcolor("black")
screen.title("Space Invaders")
screen.tracer(0)

player = Player()
scoreboard = Scoreboard()

bullets = []
is_bullet_ready = True
BULLET_COOLDOWN = 20
cooldown_counter = 0

ALIEN_ROWS = 5
ALIEN_COLUMNS = 8
ALIEN_START_X = -210
ALIEN_START_Y = 250
ALIEN_COLUMN_SPACING = 60
ALIEN_ROW_SPACING = 40
SCREEN_LEFT_EDGE = -380
SCREEN_RIGHT_EDGE = 380
aliens = []
alien_direction = 1

ALIEN_BASE_SPEED = 5
ALIEN_SPEED_INCREMENT = 1
alien_speed = ALIEN_BASE_SPEED

ALIEN_HIT_DISTANCE = 15
PLAYER_HIT_DISTANCE = 20
GAME_OVER_LINE_Y = player.ycor() + 30

BARRIER_HIT_DISTANCE = 20
BARRIER_CENTERS_X = [-270, -90, 90, 270]
BARRIER_Y_START = -150
BARRIER_ROWS = 3
BARRIER_COLUMNS = 4
SEGMENT_SPACING = 12
barriers = []



def create_barriers():
    for center_x in BARRIER_CENTERS_X:
        for row in range(BARRIER_ROWS):
            for col in range(BARRIER_COLUMNS):
                x = center_x + (col - BARRIER_COLUMNS / 2) * SEGMENT_SPACING
                y = BARRIER_Y_START - row * SEGMENT_SPACING
                segment = Barrier(x, y)
                barriers.append(segment)

create_barriers()

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
                alien.hideturtle()
                aliens.remove(alien)
                scoreboard.increase_score(10)
                break


def check_alien_player_collision():
    global game_is_on
    for alien in aliens:
        if alien.distance(player) < PLAYER_HIT_DISTANCE or alien.ycor() < GAME_OVER_LINE_Y:
            game_is_on = False
            scoreboard.game_over()
            break


def create_fleet():
    for row in range(ALIEN_ROWS):
        for col in range(ALIEN_COLUMNS):
            x = ALIEN_START_X + col * ALIEN_COLUMN_SPACING
            y = ALIEN_START_Y - row * ALIEN_ROW_SPACING
            new_alien = Alien(x, y)
            aliens.append(new_alien)

create_fleet()

def fire_bullet():
    global is_bullet_ready
    if is_bullet_ready:
        new_bullet = Bullet(player.xcor(), player.ycor() + 10)
        bullets.append(new_bullet)
        is_bullet_ready = False


def check_level_complete():
    global alien_speed
    if not aliens:
        alien_speed += ALIEN_SPEED_INCREMENT
        scoreboard.next_level()
        create_fleet()


def restart_game():
    global game_is_on, alien_direction, alien_speed

    if game_is_on:
        return

    for bullet in bullets:
        bullet.hideturtle()
    bullets.clear()

    for alien in aliens:
        alien.hideturtle()
    aliens.clear()

    for segment in barriers:
        segment.hideturtle()
    barriers.clear()

    player.reset_position()
    scoreboard.reset()

    alien_direction = 1
    alien_speed = ALIEN_BASE_SPEED

    create_fleet()
    create_barriers()

    game_is_on = True

game_is_on = True

screen.listen()
screen.onkey(player.move_left, "Left")
screen.onkey(player.move_right, "Right")
screen.onkey(fire_bullet, "space")
screen.onkey(restart_game, "r")


try:
    while True:
        time.sleep(0.02)
        screen.update()

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

        # --- aliens movement ---
        reached_edge = False
        for alien in aliens:
            alien.move_sideways(alien_direction, ALIEN_BASE_SPEED)
            if alien.xcor() > SCREEN_RIGHT_EDGE or alien.xcor() < SCREEN_LEFT_EDGE:
                reached_edge = True

        if reached_edge:
            alien_direction *= -1
            for alien in aliens:
                alien.move_down()

        # --- collisions ---
        check_bullet_barrier_collision()
        check_bullet_alien_collision()
        check_alien_barrier_collision()
        check_alien_player_collision()
        check_level_complete()

except (turtle.Terminator, tkinter.TclError):
    pass
