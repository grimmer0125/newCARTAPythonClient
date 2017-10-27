# https://github.com/hharnisc/python-meteor

import sys
is_py2 = sys.version[0] == '2'
if is_py2:
    print("use python 2")
    import Queue as queue
    # from Tkinter import *
else:
    print("use python 3")
    import queue as queue
    # from tkinter import *

import time
from datetime import datetime
import base64
import sys
print(sys.version)
print(sys.executable)

from lib.meteor.MeteorClient import MeteorClient
# import sessionmanager as SessionManager
from sessionmanager import SessionManager
import imagecontroller as ImageController
import filebrowser as FileBrowser
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib
import io
from helper import *

print("load client.py start")


# window = None
# window=Tk()

####  grimmer's experiment
getSessionCmd = "getSessionId"
command_REGISTER_IMAGEVIEWER = '/CartaObjects/ViewManager:registerView'
command_SELECT_FILE_TO_OPEN = '/CartaObjects/ViewManager:dataLoaded'
command_REQUEST_FILE_LIST = '/CartaObjects/DataLoader:getData'
GET_IMAGE = 'GET_IMAGE'
connect_response = "connect_response"

# img = mpimg.imread('2.png')  #3s
#     # img = mpimg.imread('1.jpg') 3s
#
# imgplot = plt.imshow(img)
# plt.ion()
# plt.show()=

# client.subscribe('publicLists')
# getSession()
# client.subscribe('tasks')

# will launch matplotlib
class Client():
    def __init__(self, session = None):
        self.m_client = MeteorClient('ws://127.0.0.1:3000/websocket')
        self.controllerID = None
        self.use_other_session = False
        self.session_manager = SessionManager()
        if session != None:
            self.session_manager.use_other_session(session)
            self.use_other_session = True
        # print("test:{}".format(testtest))
        # self.sefSessionID = None
        # self.controllerID = None
        # https://stackoverflow.com/questions/43471696/sending-data-to-a-thread-in-python
        self.queue = queue.Queue()

        self.numberOfImages = 0
        self.debug_image_queue = None
        # self.testimage = 0

        # if isnotebook():
        #     print("is notebook")

        # import matplotlib
        # matplotlib.use('TkAgg')
        # sys.exit()

        if run_from_interactive():
            print("is ipython, setup matplotlib")
            plt.ion()
            plt.figure()
            plt.show()
        else:
            print("not ipython")
            # matplotlib.use('TkAgg')
            # self.window = Tk()
            # self.window.mainloop()

    def setup_debug_image_queue(self, queue):
        self.debug_image_queue = queue

    def start_connection(self):
        self.m_client.on('removed', self.removed)
        self.m_client.on('changed', self.changed)
        self.m_client.on('subscribed', self.subscribed)
        self.m_client.on('unsubscribed', self.unsubscribed)
        self.m_client.on('added', self.added)
        self.m_client.on('connected', self.connected)
        self.m_client.on('logged_in', self.on_logged_in)
        self.m_client.connect()
        while True:
            try:
                print("wait for connect resp")
                # time.sleep(0.02)
                resp = self.queue.get()
                print("get connect resp:{}".format(resp))
                break
                # check the queue
            except KeyboardInterrupt:
                break

    # def stop_connection(self):
    #     #TODO: unscribe, logout, close
    #
    # def request_file_list(self):
    #     #TODO:

    def requset_file_list(self):
        FileBrowser.queryServerFileList(self.session_manager.get(), self.m_client)
        while True:
            try:
                print("wait for request file resp")
                # time.sleep(0.02)
                resp = self.queue.get()
                print("get request file resp:{}".format(resp))
                break
                # check the queue
            except KeyboardInterrupt:
                break

    def request_file_show(self, file):
        ImageController.selectFileToOpen(self.session_manager.get(), self.m_client, self.controllerID, file)

    def subscribed(self, subscription):
        print('* SUBSCRIBED {}'.format(subscription))

    def unsubscribed(self, subscription):
        print('* UNSUBSCRIBED {}'.format(subscription))

    def remove_callback(self, error, data):
        print("in self.remove_callback")
        if error:
            print(error)
            return
        print(data)

    def remove_image_callback(self, error, data):
        print("in remove_image_callback")
        if error:
            print(error)
            return
        print("in remove_image_callback ok")
        # print(data)

    def insert_callback(self, error, data):
        print("insert callback")
        if error:
            print(error)
            return
        print("insert callback ok")
        # docs = client.find(collection, selector={'sessionID': sessionID})

        # print(data)

    def update_callback(self, error, data):
        print("update callback")
        if error:
            print(error)
            return
        print("udpate callback ok")
        # print(data)

    # python client seems to have no Optimistic update on py-client https://www.meteor.com/tutorials/blaze/security-with-methods
    def saveDataToCollection(self, collection, newDocObject, actionType):
        sessionID = self.session_manager.get()
        docs = self.m_client.find(collection, selector={'sessionID': sessionID})
        total = len(docs)
        if total > 0:
            print("try to replace first image in mongo, total images:", total)
            doc = docs[0]
            docID = doc["_id"]
            newDocObject["sessionID"] = sessionID
            # update, not test yet
            self.m_client.update(collection, {'_id': docID}, newDocObject, callback=self.update_callback)
        else:
            # insert
            print("try to to insert images")
            newDocObject["sessionID"] = sessionID
            self.m_client.insert(collection, newDocObject, callback=self.insert_callback)
            print("end to insert")

            #     newDocObject.sessionID = sessionID;
            #const docID = collection.insert(newDocObject);

        # save to mongo , imagecontroller
        # mongoUpsert(ImageController, { imageURL: url }, GET_IMAGE);
        # const url = `data:image/jpeg;base64,${buffer}`;
        # console.log('image url string size:', url.length);
    # fields are changed fields

    def render_received_image(self, imgString):
        print("render_received_image")

        imgdata = base64.b64decode(imgString)

        # NOTE: since we have tk+matplotlib for debugging, so no more saving images to files
        # print("try to save image")
        # currentTime = str(datetime.now())
        # print("currentTime:", currentTime)
        # filename = currentTime +".jpg"
        # with open(filename, 'wb') as f:
        #     f.write(imgdata)
        # print("end to save image")

        i = io.BytesIO(imgdata)
        i = mpimg.imread(i, format='JPG')  # from memory, binary

        if run_from_interactive():
            # plt.imshow(i, interpolation='nearest')
            imgplot = plt.imshow(i)# may be no difference
            plt.pause(0.01)
        else:
            print("not ipython, so do no show image after saving")
            self.debug_image_queue.put(i)
    def handleAddedOrChanged(self, collection, id, fields):
        for key, value in fields.items():
            print('  - FIELD {}'.format(key))
            # print('  - FIELD {} {}'.format(key, value))

        if collection == "users":
            print("grimmer users added/changed ")
        elif collection == "responses":
            print("grimmer responses added/changed, self_sessionID:", fields["sessionID"])

            if "pushedImage" in fields:
                print("get image") # handle images
                # if "buffer" in fields:
                imgString = fields["buffer"]
                imageLeng = len(imgString)
                print("image data size in command response:", imageLeng)

                #TODO the dummy empty images should be solved in the future, but now we use it to judge connect ok
                if imageLeng > 10012:
                    # url = "data:image/jpeg;base64,"+imgString
                    # save to mongo for share screen
                    #TODO python: forget to setup controllerID. js: forget to add size
                    self.saveDataToCollection('imagecontroller', { "imageURL": imgString, "size": len(imgString) }, GET_IMAGE)
                    #save file for testing
                    # print("try to save image")
                    # self.render_received_image(imgString)

                    # imgdata = base64.b64decode(imgString)
                    # filename = currentTime +".jpg"  # I assume you have a way of picking unique filenames
                    # with open(filename, 'wb') as f:
                    #     f.write(imgdata)
                    #
                    #     if run_from_interactive():
                    #         # img = mpimg.imread('1.jpg'), from file
                    #         i = io.BytesIO(imgdata)
                    #         i = mpimg.imread(i, format='JPG') # from memory, binary
                    #
                    #         # plt.imshow(i, interpolation='nearest')
                    #         #TODO let mainthread to redraw
                    #         imgplot = plt.imshow(i)# may be no difference
                    #         plt.pause(0.01)
                    #     else:
                    #         print("not ipython, so do no show image after saving")

                # global numberOfImages
                self.numberOfImages += 1
                if self.numberOfImages == 2:
                    print("get dummy 2 images. start to request testing image, aj.fits")
                    self.queue.put(connect_response)
            elif "cmd" in fields:
                cmd = fields["cmd"]
                print("cmd respone:{}".format(cmd))

                #1. TODO handle it
                if cmd == command_REGISTER_IMAGEVIEWER:
                    print("response:REGISTER_IMAGEVIEWER")
                    data = fields["data"] # save controllerID to use
                    # will send setSize inside
                    self.controllerID = data
                    ImageController.parseReigsterViewResp(self.m_client, data)
                elif cmd == command_REQUEST_FILE_LIST:
                    print("response:REQUEST_FILE_LIST:")
                    data = fields["data"]
                    files = data["dir"]
                    rootDir= data["name"]
                    print("files:{};dir:{}".format(files, rootDir))
                    print("response:REQUEST_FILE_LIST end")
                    self.queue.put("get file list resp")
                elif cmd == command_SELECT_FILE_TO_OPEN:
                    print("response:SELECT_FILE_TO_OPEN")
            #2.  remove it, may not be necessary for Browser, just alight with React JS Browser client
            self.m_client.remove('responses', {'_id': id}, callback=self.remove_callback)

        elif collection == "imagecontroller":
            print("grimmer imagecontroller added/changed")
            sessionID = self.session_manager.get()
            docs = self.m_client.find(collection, selector={'sessionID': sessionID})
            total = len(docs)
            if total > 0:
                print("total doc:",total)
                # firstDoc = docs[0]
                for doc in docs:
                    docID = doc["_id"]
                    print("loop image collection, id is", docID)
                    #NOTE since meteor-python does not have Optimistic update so that we need to remove old images after getting added/changed callback
                    if docID != id:
                        print("remove one image document")
                        self.m_client.remove('imagecontroller', {'_id': docID}, callback=self.remove_image_callback)
                        # global testimage
                        # testimage +=1
                        # if testimage ==1:
                        #     print("try 2nd image file")
                        #     ImageController.selectFileToOpen2(client)
                        #
                        # doc["comments"] = "apple"
                        # for testing client.update('imagecontroller', {'_id': docID}, {"name": "ggg"}, callback=update_callback)
                        # for testing
                        # client.update('imagecontroller', {'_id': docID}, doc, callback=update_callback)
                    else:
                        print("not remove it")
                        print("image size in collection:", len(doc["imageURL"]))
                        self.render_received_image(doc["imageURL"])

                        # delete previous images

    #TODO commmand response need to be deleted.
    def added(self, collection, id, fields):
        print('* ADDED {} {}'.format(collection, id))
        self.handleAddedOrChanged(collection, id, fields)
        print('end added')


    #  ADDED users vo5Eb7cG94waZmiGY
    #   - FIELD username grimmer4

        # query the data each time something has been added to
        # a collection to see the data `grow`
        # all_lists = client.find('lists', selector={})
        # print('Lists: {}'.format(all_lists))
        # print('Num lists: {}'.format(len(all_lists)))

        # if collection == 'list' you could subscribe to the list here
        # with something like
        # client.subscribe('todos', id)
        # all_todos = client.find('todos', selector={})
        # print 'Todos: {}'.format(all_todos)

        # all_lists = client.find('tasks', selector={})
        # print('Tasks: {}'.format(all_lists))
        # print('Num lists: {}'.format(len(all_lists)))

    def changed(self, collection, id, fields, cleared):
        print('CHANGED !!!: {} {}'.format(collection, id))
        handleAddedOrChanged(collection, id, fields) # only take effect when JS changes rendered image

        # all_lists = client.find('tasks', selector={})
        # print('Tasks: {}'.format(all_lists))
        # print('Num lists: {}'.format(len(all_lists)))
        print('end changed')



        # conf.set('ddp', 'token', data['token'])
        # conf.update()

    def subscription_response_callback(self, error):
        if error:
            print("sub fail")
            print(error)
        print("sub resp ok")

    def subscription_image_callback(self, error):
        if error:
            print("sub2 fail")
            print(error)
        print("sub image ok2")
        if self.use_other_session == False:
            ImageController.sendRegiserView(self.session_manager.get(), self.m_client)

    def setup_subscription(self):
        print("get:", self.session_manager.get())

        if self.use_other_session == False:
            self.m_client.subscribe('commandResponse', [self.session_manager.get()], callback=self.subscription_response_callback)

        self.m_client.subscribe('imagecontroller', [self.session_manager.get()], callback=self.subscription_image_callback)
    def getSession_callback(self, error, result):
        if error:
            print("getSession_callback error")
            print(error)
            return
        print("in getSession_callback")
        print(result)
        if self.use_other_session == False:
            self.session_manager.set(result)
        # subscribe response
        # subscribe imageController
        # observe response, imageController
        self.setup_subscription()

    def getSession(self):
        print("try getSession")
        print("setupt subscription callback")

        # empty params, so []
        self.m_client.call(getSessionCmd, [], self.getSession_callback)

    def connected(self):
        print('* CONNECTED')
        # all_lists = client.find('tasks', selector={})
        # print('Tasks: {}'.format(all_lists))
        # print('Num lists: {}'.format(len(all_lists)))
        if self.use_other_session == False:
            print('setup subscribe collection in session callback')
            self.getSession()
        else:
            self.setup_subscription()
            self.queue.put(connect_response)
        print('end connected, try login')
        self.m_client.login('grimmer4', "1234")

    def removed(self, collection, id):
        print('* REMOVED {} {}'.format(collection, id))

    def on_logged_in(self, data):
        print('LOGGIN IN', data)

print("load client end")
# (sort of) hacky way to keep the client alive
# ctrl + c to kill the script
# while True:
#     try:
#         time.sleep(5)
#     except KeyboardInterrupt:
#         break
