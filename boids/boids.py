from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from random import uniform, random
from time import sleep
from vector_2d import Vector
from math import cos, sin, sqrt


def distance(vector_a, vector_b):
    return sqrt((vector_a.x-vector_b.x)**2-(vector_a.y-vector_b.y)**2)

def bound(val, lim):
    if val > lim:
        return val - lim
    elif val < 0:
        return lim + val
    else:
        return val


class Boid:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def update(self):
        self.position += self.velocity.normal()


class Flock:
    def __init__(self, plot, points, angles, xlim, ylim):
        self.plot = plot

        self.xlim, self.ylim = xlim, ylim
        self.boids = [Boid(Vector(point[0], point[1]), Vector(cos(angle), sin(angle))) for point, angle in
                      zip(points, angles)]

    def separation(self):
        for i, boid_i in enumerate(self.boids):
            for j, boid_j in enumerate(self.boids):
                if i != j:
                    distance = sqrt((boid_i.position.x - boid_j.position.x) ** 2 +
                                    (boid_i.position.y - boid_j.position.y) ** 2)
                    if distance < 10.0:
                        boid_i.velocity += (boid_i.position - boid_j.position).normal()

    def alignment(self):
        average_velocity = Vector(sum([boid.velocity.x for boid in flock.boids]),
                                  sum([boid.velocity.x for boid in flock.boids])) / len(flock.boids)
        for boid in self.boids:
            boid.velocity += average_velocity.normal()

    def cohesion(self):
        average_position = Vector(sum([boid.position.x for boid in flock.boids]),
                                  sum([boid.position.x for boid in flock.boids])) / len(flock.boids)
        for boid in self.boids:
            boid.velocity += (average_position - boid.position).normal()

    def tick(self, frames):
        self.separation()
        self.alignment()
        self.cohesion()
        for boid in self.boids:
            boid.update()
            boid.position = Vector(bound(boid.position.x, self.xlim), bound(boid.position.y, self.ylim))
        xs = [boid.position.x for boid in self.boids]
        ys = [boid.position.y for boid in self.boids]
        self.plot.set_offsets(np.array(list(zip(xs, ys))))
        sleep(0.1)
        return self.plot

xlim = 100
ylim = 200
N = 50
xs = [uniform(0,xlim) for _ in range(N)]
ys = [uniform(0,ylim) for _ in range(N)]
angles = [random() for _ in range(N)]
points = list(zip(xs,ys))
fig = plt.figure()
ax = plt.axes(xlim=(0, xlim), ylim=(0, ylim))
scatter_plot = ax.scatter([p[0] for p in points], [p[1] for p in points])

flock = Flock(scatter_plot, points, angles, xlim, ylim)

anim = FuncAnimation(fig, flock.tick, interval=10)

plt.show()

