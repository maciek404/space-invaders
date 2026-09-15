from turtle import Turtle
from theme import BULLET_COLOR

BULLET_MOVE_DISTANCE = 10


class Bullet(Turtle):
    def __init__(self, start_x, start_y, color, heading=90):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=0.2, stretch_len=0.5)
        self.setheading(heading)
        self.penup()
        self.goto(start_x, start_y)

    def move(self):
        self.forward(BULLET_MOVE_DISTANCE)

    def is_off_screen(self, screen_top_boundary=290, screen_bottom_boundary=-290):
        return self.ycor() > screen_top_boundary or self.ycor() < screen_bottom_boundary

