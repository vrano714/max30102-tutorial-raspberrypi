#-*-coding:utf-8-*-

import matplotlib.pyplot as plt
import numpy as np

# load log data
red = []
with open("./red.log", "r") as f:
    for r in f:
        red.append(int(r))

ir = []
with open("./ir.log", "r") as f:
    for r in f:
        ir.append(int(r))

# x-axis values
x = np.arange(len(red))

fig = plt.figure()
ax = fig.add_subplot(111)

# RED LED
ax.plot(x, red, c="red", label="RED LED")
# IR LED (decrease values to show near RED LED)
ax.plot(x, np.array(ir)-20000, c="orange", label="IR LED (shifted)")

# modify limits
ax.set_ylim(122000, 126000)
# ax.set_xlim(400,600)

# show legend
ax.legend(loc="best")

plt.show()
