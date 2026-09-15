import random
from turtle import Turtle
from theme import STAR_COLORS

STAR_COUNT = 80

SCREEN_LEFT = -390
SCREEN_RIGHT = 390
SCREEN_TOP = 290
SCREEN_BOTTOM = -290


class Starfield(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self._draw_stars()

    def _random_position(self):
        x = random.randint(SCREEN_LEFT, SCREEN_RIGHT)
        y = random.randint(SCREEN_BOTTOM, SCREEN_TOP)
        return x, y

    def _draw_stars(self):
        for _ in range(STAR_COUNT):
            x, y = self._random_position()
            size = random.choice([2, 2, 2, 3, 4])
            color = random.choice(STAR_COLORS)
            self.goto(x, y)
            self.dot(size, color)