from turtle import Turtle

STARTING_POSITION = (0, -260)
MOVE_DISTANCE = 20
SCREEN_LEFT_BOUNDARY = -360
SCREEN_RIGHT_BOUNDARY = 360

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("triangle")
        self.color("white")
        self.shapesize(stretch_wid=1, stretch_len=1.5)
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
