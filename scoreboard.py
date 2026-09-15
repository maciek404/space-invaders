from turtle import Turtle
from theme import TEXT_COLOR, GAME_OVER_COLOR

FONT = ("Courier", 16, "normal")
GAME_OVER_FONT = ("Courier", 24, "bold")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.level = 1
        self.hideturtle()
        self.penup()
        self.update_display()

    def update_display(self):
        self.clear()
        self.color(TEXT_COLOR)
        self.goto(0, 260)
        self.write(f"Score: {self.score}    Level: {self.level}", align="center", font=FONT)

    def increase_score(self, points):
        self.score += points
        self.update_display()

    def next_level(self):
        self.level += 1
        self.update_display()

    def game_over(self):
        self.color(GAME_OVER_COLOR)
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=GAME_OVER_FONT)
        self.goto(0, -45)
        self.write("Press R to restart", align="center", font=FONT)

    def reset(self):
        self.score = 0
        self.level = 1
        self.update_display()
