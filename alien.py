from turtle import Turtle

ALIEN_DROP_DISTANCE = 30

SHAPE_NAME = "alien_invader"
# SHAPE_POINTS = (
#     (-15, 6), (-9, 6), (-6, 12), (0, 7),
#     (6, 12), (9, 6), (15, 6),
#     (11, -2), (6, -2), (4, -10),
#     (0, -6), (-4, -10), (-6, -2), (-11, -2),
# )
SHAPE_POINTS = (
    (-21, 4), (-14, 11), (-6, 8), (0, 12),
    (6, 8), (14, 11), (21, 4),
    (15, -5), (8, -2), (6, -9),
    (0, -5), (-6, -9), (-8, -2), (-15, -5),
)


def register_alien_shape(screen):
    screen.register_shape(SHAPE_NAME, SHAPE_POINTS)


class Alien(Turtle):
    def __init__(self, x, y, color):
        super().__init__()
        self.shape(SHAPE_NAME)
        self.setheading(270)
        self.color(color)
        self.penup()
        self.goto(x, y)

    def move_sideways(self, direction, speed):
        new_x = self.xcor() + speed * direction
        self.goto(new_x, self.ycor())

    def move_down(self):
        self.goto(self.xcor(), self.ycor() - ALIEN_DROP_DISTANCE)
        
