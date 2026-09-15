from turtle import Turtle

PARTICLE_COUNT = 8
PARTICLE_SPEED = 6
LIFESPAN_FRAMES = 12
START_SIZE = 0.5
MIN_SIZE = 0.05


class Explosion:
    def __init__(self, x, y, color):
        self._frame = 0
        self._particles = []

        for i in range(PARTICLE_COUNT):
            angle = i * (360 / PARTICLE_COUNT)
            particle = Turtle()
            particle.shape("circle")
            particle.color(color)
            particle.shapesize(stretch_wid=START_SIZE, stretch_len=START_SIZE)
            particle.penup()
            particle.setheading(angle)
            particle.goto(x, y)
            self._particles.append(particle)

    def is_finished(self):
        return self._frame >= LIFESPAN_FRAMES

    def update(self):
        self._frame += 1

        if self._frame >= LIFESPAN_FRAMES:
            for particle in self._particles:
                particle.hideturtle()
            return

        shrink_progress = self._frame / LIFESPAN_FRAMES
        current_size = max(START_SIZE * (1 - shrink_progress), MIN_SIZE)

        for particle in self._particles:
            particle.forward(PARTICLE_SPEED)
            particle.shapesize(stretch_wid=current_size, stretch_len=current_size)

    def force_finish(self):
        for particle in self._particles:
            particle.hideturtle()
        self._frame = LIFESPAN_FRAMES

