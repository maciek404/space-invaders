from turtle import Turtle
from theme import BARRIER_COLOR

SEGMENT_COLOR = BARRIER_COLOR
BARRIER_SHAPE_MASK = [
    [0, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 1, 1],
]


class Barrier(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("square")
        self.color(SEGMENT_COLOR)
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.penup()
        self.goto(x, y)

