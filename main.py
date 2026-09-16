from turtle import Screen

import theme
from player import register_player_shape
from alien import register_alien_shape
from game import Game

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor(theme.BACKGROUND_COLOR)
screen.title("Space Invaders")
screen.tracer(0)

register_player_shape(screen)
register_alien_shape(screen)

game = Game(screen)
game.run()

