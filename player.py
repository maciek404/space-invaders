from turtle import Turtle
from theme import PLAYER_COLOR

STARTING_POSITION = (0, -260)
MOVE_DISTANCE = 20
SCREEN_LEFT_BOUNDARY = -360
SCREEN_RIGHT_BOUNDARY = 360

SHAPE_NAME = "player_ship"
SHAPE_POINTS = (
    (0, 18), (5, 5), (18, 0), (8, -4),
    (5, -15), (0, -8), (-5, -15),
    (-8, -4), (-18, 0), (-5, 5),
)

def register_player_shape(screen):
    screen.register_shape(SHAPE_NAME, SHAPE_POINTS)

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape(SHAPE_NAME)
        self.color(PLAYER_COLOR)
        self.setheading(90)
        self.penup()
        self.goto(STARTING_POSITION)

    def move_left(self):
        if self.xcor() > SCREEN_LEFT_BOUNDARY:
            new_x = self.xcor() - MOVE_DISTANCE
            self.goto(new_x, self.ycor())

    def move_right(self):
        if self.xcor() < SCREEN_RIGHT_BOUNDARY:
            new_x = self.xcor() + MOVE_DISTANCE
            self.goto(new_x, self.ycor())

    def reset_position(self):
        self.goto(STARTING_POSITION)
