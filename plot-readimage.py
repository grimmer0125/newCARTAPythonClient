# https://github.com/hharnisc/python-meteor
import time

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
img=mpimg.imread('1.jpg')
imgplot = plt.imshow(img)
# plt.ion() #intetactively , or 2. plt.draw() (nonblocking? no effect in termianl, in code?)
# plt.show(block=False) can replace .ion()
plt.show()

print("after showing")

# time.sleep(5)
#
# time.sleep(5)
#
# time.sleep(5)
#
# time.sleep(5)
#
# time.sleep(5)

# (sort of) hacky way to keep the client alive
# ctrl + c to kill the script
while True:
    try:
        time.sleep(5)
        print("sleep 5s")
    except KeyboardInterrupt:
        break
