from helper import *

from threading import Timer
import threading

image_q = None

class DebugWorker(threading.Thread):
    def __init__(self, task=None):
        if task is None:
            task = self.dummy_task
        threading.Thread.__init__(self)
        self.task = task
        # self.seconds = seconds
        self.stopped = threading.Event()
    def dummy_task(self):
        print("hello DebugWorker!")
        # timer thread
        print(threading.current_thread().__class__.__name__)

    def run(self):
        print("start another thread:")
        print(threading.current_thread().__class__.__name__)
        # img=mpimg.imread('1.jpg')
        # imgplot = plt.imshow(img)
        # plt.show()
        self.task()
        print("after showing")
    def stop(self):
        self.stopped.set()

# import matplotlib
# matplotlib.use('TkAgg')
import sys
is_py2 = sys.version[0] == '2'
if is_py2:
    print("use python 2")
    import Queue as queue
    from Tkinter import *
else:
    print("use python 3")
    import queue as queue
    from tkinter import *

def run_test():
    from client import Client
    # in another thread/process to test
    c = Client("test", "test")
    if image_q is None:
        print("ignore g!!!!!!!!!")
    else:
        print("image queue in client")
        c.setup_debug_image_queue(image_q)
        # print("start cartaclient example2")
    # c.setup_url("acdc0.asiaa.sinica.edu.tw:47569")
    c.start_connection()
    c.files().request_file_list()
    c.request_file_show("cube_x220_z100_17MB-20.fits") #aJ

    c2 = Client("test", "test")
    if image_q is None:
        print("ignore g!!!!!!!!!")
    else:
        # print("image queue in client")
        c2.setup_debug_image_queue(image_q)
        # print("start cartaclient example2")
    # c.setup_url("acdc0.asiaa.sinica.edu.tw:47569")
    c2.start_connection()
    c2.files().request_file_list()
    c2.request_file_show("cube_x220_z100_17MB-19.fits")
def main():
    print("start cartaclient example")

    # window = None
    # Create a window

    # w = Label(window, text="Hello World")
    # w.pack()
    # window = Tk()
    # window.mainloop()
    if run_from_interactive() == FALSE:
        print("in python program mode, create tk window to debug")
        global window
        window = Tk() # should executed before importing matplotlib
        w = Label(window, text="Hello World")
        w.pack()

        import matplotlib
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg

        # matplotlib.use('TkAgg')
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

        # ref:
        # https://stackoverflow.com/questions/34764535/why-cant-matplotlib-plot-in-a-different-thread
        # https://hardsoftlucid.wordpress.com/various-stuff/realtime-plotting/
        # https://github.com/IGITUGraz/live-plotter#notes-about-backends
        global line, canvas, ax, image_q
        # fig = matplotlib.figure.Figure()
        fig = plt.figure()

        # ax = fig.add_subplot(1, 1, 1)
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.show()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        # line, = ax.plot([1, 2, 3], [1, 2, 10])

        if FALSE:
            print("got it0")
            img=mpimg.imread('1.jpg')
            print("got it00")
            imgplot = plt.imshow(img)
            print("got it000")
            # plt.show() //some problems
            # canvas.draw()
            print("got it")

        ## TODO change to image_q
        def update_debug_plot(q):
            try:  # Try to check if there is data in the queue
                # print("start to polling image data")
                result = q.get_nowait()

                if result != 'Q':
                    print("get image data in queue")
                    # print result

                    # import matplotlib
                    # import matplotlib.pyplot as plt
                    # import matplotlib.image as mpimg

                    imgplot = plt.imshow(result)  # may be no difference
                    print("get image data in queue2")
                    # plt.pause(0.01)
                    print("get image data in queue3")

                    #  line.set_ydata([1,result,10])
                    #  ax.draw_artist(line)
                    canvas.draw()
                    window.after(200, update_debug_plot, q)
                else:
                    print('no queue done')
            except:
                # print("empty")
                window.after(200, update_debug_plot, q)

        image_q = queue.Queue()
        # run_test()

        update_debug_plot(image_q) # here to poll data from cleint
        # run_test(q) to run functions of client in another thread
        print("current thread:")
        print(threading.current_thread().__class__.__name__)

        d = DebugWorker(run_test)
        d.start()


        print('before mainloop')
        window.mainloop()
        print('Done')
    else:
        print('in interactive python interpreter')
        run_test()

if __name__ == '__main__':
    main()
    # (sort of) hacky way to keep the client alive
    # ctrl + c to kill the script
    # while True:
    #     try:
    #         time.sleep(5)
    #     except KeyboardInterrupt:
    #         break
