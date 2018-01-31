#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as np

# https://matplotlib.org/examples/animation/basic_example.html
# def update_line(num, data, line):
#     line.set_data(data[..., :num])
#     return line,
# fig1 = plt.figure()
# data = np.random.rand(2, 25)
# l, = plt.plot([], [], 'r-')
# plt.xlim(0, 1)
# plt.ylim(0, 1)
# plt.xlabel('x')
# plt.title('test')
# line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(data, l),
#                                    interval=50, blit=True)
# To save the animation, use the command: line_ani.save('lines.mp4')

# fig2 = plt.figure()
# x = np.arange(-9, 10)
# y = np.arange(-9, 10).reshape(-1, 1)
# base = np.hypot(x, y)
# ims = []
# for add in np.arange(15):
#     ims.append((plt.pcolor(x, y, base + add, norm=plt.Normalize(0, 30)),))
# im_ani = animation.ArtistAnimation(fig2, ims, interval=50, repeat_delay=3000,
#                                    blit=True)
# To save this second animation with some metadata, use the following command:
# im_ani.save('im.mp4', metadata={'artist':'Guido'})

# https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
print("before show")
plt.axis([-50,50,0,10000])

# ion(): seems drawing will be in another process, 
# previous drawing setup will not effect in python script mode (ipython will), 
# only the code below this line
plt.ion()

# plt.draw()
# plt.show(block = False)     # Add block = False
# print("run show")
plt.show()

print("after show")

x = np.arange(-50, 51)
for pow in range(1,5):   # plot x^1, x^2, ..., x^4
    y = [Xi**pow for Xi in x]
    plt.plot(x, y)
    plt.draw()
    plt.pause(0.001)
    # input("Press [enter] to continue.")

# plt.show()
print("after show2")

#
while True:
    try:
        time.sleep(5)
        print("sleep 5s")
    except KeyboardInterrupt:
        break
