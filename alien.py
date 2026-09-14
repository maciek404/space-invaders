from turtle import Turtle

ALIEN_DROP_DISTANCE = 30


class Alien(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("circle")
        self.color("green")
        self.penup()
        self.goto(x, y)

    def move_sideways(self, direction, speed):
        new_x = self.xcor() + speed * direction
        self.goto(new_x, self.ycor())

    def move_down(self):
        self.goto(self.xcor(), self.ycor() - ALIEN_DROP_DISTANCE)
        
