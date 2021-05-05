import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import sleep
import sys


def grid_update(i, img, input_grid):
    max_x, max_y = input_grid.shape
    output_grid = input_grid.copy()
    padded_grid = np.pad(input_grid, 1)
    for x in range(max_x):
        for y in range(max_y):
            total = padded_grid[x, y]+padded_grid[x+1, y]+padded_grid[x+2, y]+padded_grid[x, y+1] + \
                padded_grid[x+2, y+1]+padded_grid[x, y+2] + \
                padded_grid[x+1, y+2]+padded_grid[x+2, y+2]
            if output_grid[x, y] == 1:
                if total < 2 or total > 3:
                    output_grid[x, y] = 0
            elif output_grid[x, y] == 0:
                if total == 3:
                    output_grid[x, y] = 1
    input_grid[:] = output_grid[:]
    img.set_data(output_grid)
    return img


with open(sys.argv[1], 'r') as f:
    grid = np.array(list(map(lambda line: [int(char) for char in line], list(
        map(list, f.read().splitlines())))))


fig, ax = plt.subplots()
img = ax.imshow(grid, cmap='Greys')

anim = animation.FuncAnimation(fig, grid_update, fargs=(img, grid,))

plt.show()
