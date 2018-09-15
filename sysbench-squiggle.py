#!/usr/bin/python3

import re
import sys
import time
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import select
from scipy import interpolate
import subprocess

parser = argparse.ArgumentParser(description='Sysbench Squiggly Line Generator')
parser.add_argument('command', metavar='CMD', help='Sysbench command to execute')
args = parser.parse_args()

# Create the figure
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
ax.grid()

# Number of data points
n_samples = 25

# The actual data
y = np.arange(0, n_samples, 1)
x = np.arange(0, n_samples, 1)

# Smoothed values use to display the value
dy = np.linspace(0, n_samples, 100)
dx = np.linspace(0, n_samples, 100)

y_max = np.amax(y) * 1.3

# Set labels and X axis limits (makes the line prettier)
ax.set_ylabel('QPS')
ax.set_xlim(0, 24)

lines = []
texts = []
infile = None

def init():  # only required for blitting to give a clean slate.
    line.set_ydata([np.nan] * len(dx))
    return line,


def animate(i):
    global y
    global infile
    global texts
    global y_max

    if infile is None:
        time.sleep(0.1)
        ax.figure.canvas.draw()
        return lines + texts, ax

    # Only read if there's data in stdin
    #r = select.select([infile], [], [], 0.1)[0]
    #if len(r) > 0:

    #line = lines[-1]

    l = infile.readline()
    if len(l) == 0:
        infile = None
        # End of file, sysbench is complete
        global x, y
        for t in texts:
            t.set_text('')

        texts.append(plt.text(0.6, -0.2, 'Max QPS: ' + str(np.amax(y)), horizontalalignment='center',
                              verticalalignment='center', transform=ax.transAxes))
        y = np.arange(0, n_samples, 1)
        x = np.arange(0, n_samples, 1)
        return lines + texts, ax
    else:

        # Extract the QPS value from the output
        match = re.search(".*qps: ([0-9.]*).*", l)
        if match:
            print(match.group(1))
            y = np.delete(y, 0)
            y = np.append(y, match.group(1)).astype(np.float)

    # Scale Y axis to 130% of max Y value
    new_y_max = np.amax(y) * 1.3
    if new_y_max > y_max:
        y_max = new_y_max

    ax.set_ylim(0, y_max)
    ax.figure.canvas.draw()

    # Smooth the output
    dy = interpolate.InterpolatedUnivariateSpline(x, y)(dx)

    # Update the  data
    lines[-1].set_ydata(dy)
    return lines + texts, ax


def handle_click(event):
    global infile
    global lines
    lines += ax.plot(dx, dy)
    proc = subprocess.Popen(args.command, shell=True, universal_newlines=True, bufsize=1, stdout=subprocess.PIPE, cwd='/usr/share/sysbench')
    infile = proc.stdout


axb = plt.axes([0.1, 0.03, 0.1, 0.1])
b = Button(axb, 'Start')
b.on_clicked(handle_click)

# Start the animation which calls our `animate` callback
ani = animation.FuncAnimation(
    fig, animate, interval=10, blit=False, save_count=10)

# Display the graph
plt.show()
