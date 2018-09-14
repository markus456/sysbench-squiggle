#!/usr/bin/python3

import re
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import select
from scipy import interpolate

# Create the figure
fig, ax = plt.subplots()
ax.grid()

# Number of data points
n_samples = 25

# The actual data
y = np.arange(0, n_samples, 1)
x = np.arange(0, n_samples, 1)

# Smoothed values use to display the value
dy = np.linspace(0, n_samples, 100)
dx = np.linspace(0, n_samples, 100)

# Set labels and X axis limits (makes the line prettier)
ax.set_ylabel('QPS')
ax.set_xlim(0, 24)

# Create the plit
line, = ax.plot(dx, dy)

def init():  # only required for blitting to give a clean slate.
    line.set_ydata([np.nan] * len(dx))
    return line,


def animate(i):
    global y

    # Only read if there's data in stdin
    r = select.select([sys.stdin], [], [], 0.01)[0]
    if len(r) > 0:

        l = sys.stdin.readline()
        if len(l) == 0:
            # End of file, sysbench is complete
            return plt.text(0.5, 0.8, 'Max QPS: ' + str(np.amax(y)), horizontalalignment='center',
                            verticalalignment='center', transform=ax.transAxes), line
        else:

            # Extract the QPS value from the output
            match = re.search(".*qps: ([0-9.]*).*", l)
            if match:
                y = np.delete(y, 0)
                y = np.append(y, match.group(1)).astype(np.float)

    # Scale Y axis to 130% of max Y value
    ax.set_ylim(0, np.amax(y) * 1.3)
    ax.figure.canvas.draw()

    # Smooth the output
    dy = interpolate.InterpolatedUnivariateSpline(x, y)(dx)

    # Update the  data
    line.set_ydata(dy)
    return line,


# Start the animation which calls our `animate` callback
ani = animation.FuncAnimation(
    fig, animate, interval=1, blit=True, save_count=30)

# Display the graph
plt.show()
