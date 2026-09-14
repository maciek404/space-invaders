from turtle import Turtle

SEGMENT_COLOR = "blue"

class Barrier(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("square")
        self.color(SEGMENT_COLOR)
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.penup()
        self.goto(x, y)

