import math
import turtle
from datetime import datetime
from random import randint, uniform


class SpirographAnimator:
    def __init__(self, step):
        self.spirographs = []
        self.step = step

    def add_spirograph(self, spirograph):
        self.spirographs.append(spirograph)

    def animate(self):
        flag = any([not spirograph.is_complete()
                   for spirograph in self.spirographs])
        while flag:
            for spirograph in self.spirographs:
                if not spirograph.is_complete():
                    spirograph.update(self.step)
            flag = any([not spirograph.is_complete()
                       for spirograph in self.spirographs])


class Spirograph:
    def __init__(self, outer_radius, inner_radius, distance, color, x_center=0, y_center=0):
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius
        self.distance = distance
        self.x_center = x_center
        self.y_center = y_center
        self.rotation_number = inner_radius//math.gcd(
            inner_radius, outer_radius)

        self.complete = False
        self.angle = 0

        self.pen = turtle.Turtle()
        self.pen.color(color)
        self.pen.speed(200)
        self.pen.up()

    def update(self, step):
        if not self.complete:
            angle = math.radians(self.angle)
            self.x_position = (self.outer_radius-self.inner_radius)*math.cos(angle) + self.distance * \
                math.cos((self.outer_radius-self.inner_radius)
                         * angle/self.inner_radius)
            self.y_position = (self.outer_radius-self.inner_radius)*math.sin(angle) - self.distance * \
                math.sin((self.outer_radius-self.inner_radius)
                         * angle/self.inner_radius)
            self.pen.setpos(self.x_center+self.x_position,
                            self.x_center+self.y_position)
            if not self.pen.isdown():
                self.pen.down()
            self.angle += step
        if self.angle >= 360*self.rotation_number+1:
            self.complete = True
            self.pen.hideturtle()

    def is_complete(self):
        return self.complete


animator = SpirographAnimator(1)
for _ in range(randint(0, 10)):
    animator.add_spirograph(Spirograph(randint(0, 300), randint(0, 300), randint(0, 300), [
                            uniform(0, 1), uniform(0, 1), uniform(0, 1)], randint(-300, 300), randint(-150, 150)))
animator.animate()

filename = 'spirograph_' + datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
canvas = turtle.getcanvas()

canvas.postscript(file=filename+'.eps')
