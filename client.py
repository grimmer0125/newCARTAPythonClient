# https://github.com/hharnisc/python-meteor
from helper import *

import sys
is_py2 = sys.version[0] == '2'
if is_py2:
    dprint("use python 2")
    import Queue as queue
    # from Tkinter import *
else:
    dprint("use python 3")
    import queue as queue
    # from tkinter import *

import time
from datetime import datetime
import base64
import sys
dprint(sys.version)
dprint(sys.executable)

from lib.meteor.MeteorClient import MeteorClient
# import sessionmanager as SessionManager
from sessionmanager import SessionManager
import imagecontroller as ImageController
import filebrowser as FileBrowser
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib
import io

dprint("load client.py start")


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
    def __init__(self, user, password):
        self.url = 'ws://127.0.0.1:3000/websocket'
        self.m_client = None
        self.controllerID = None
        self.m_client = None
        self.use_other_session = False
        self.session_manager = SessionManager()
        self.user = user
        self.password = password
        self.remote_current_folder = None
        # if session != None:
        #     self.session_manager.use_other_session(session)
        #     self.use_other_session = True

        # dprint("test:{}".format(testtest))
        # self.sefSessionID = None
        # self.controllerID = None
        # https://stackoverflow.com/questions/43471696/sending-data-to-a-thread-in-python
        self.queue = queue.Queue()

        self.numberOfImages = 0
        self.debug_image_queue = None
        # self.testimage = 0

        # if isnotebook():
        #     dprint("is notebook")

        # import matplotlib
        # matplotlib.use('TkAgg')
        # sys.exit()

        if run_from_interactive():
            dprint("is ipython, setup matplotlib")
            plt.ion()
            plt.figure()
            plt.show()
        else:
            dprint("not ipython")
            # matplotlib.use('TkAgg')
            # self.window = Tk()
            # self.window.mainloop()
    def watch_other_session(self, session):
        self.session_manager.use_other_session(session)
        self.use_other_session = True

    def setup_debug_image_queue(self, queue):
        self.debug_image_queue = queue

    def setup_url(self, url):
        self.url = "ws://"+url + "/websocket"
    def start_connection(self):
        self.m_client = MeteorClient(self.url)
        self.controllerID = None
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
                print("wait for connect response")
                # time.sleep(0.02)
                resp = self.queue.get()
                dprint("get connect resp:{}".format(resp))
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
                dprint("get request file resp:{}".format(resp))
                break
                # check the queue
            except KeyboardInterrupt:
                break

    def request_file_show(self, file):
        ImageController.selectFileToOpen(self.session_manager.get(), self.m_client, self.controllerID, file, self.remote_current_folder)

    def subscribed(self, subscription):
        print('* SUBSCRIBED {}'.format(subscription))

    def unsubscribed(self, subscription):
        dprint('* UNSUBSCRIBED {}'.format(subscription))

    def remove_callback(self, error, data):
        dprint("in self.remove_callback")
        if error:
            dprint(error)
            return
        dprint(data)

    def remove_image_callback(self, error, data):
        dprint("in remove_image_callback")
        if error:
            dprint(error)
            return
        dprint("in remove_image_callback ok")
        # dprint(data)

    def insert_callback(self, error, data):
        dprint("insert callback")
        if error:
            dprint(error)
            return
        dprint("insert callback ok")
        # docs = client.find(collection, selector={'sessionID': sessionID})

        # dprint(data)

    def update_callback(self, error, data):
        dprint("update callback")
        if error:
            dprint(error)
            return
        dprint("udpate callback ok")
        # dprint(data)

    # python client seems to have no Optimistic update on py-client https://www.meteor.com/tutorials/blaze/security-with-methods
    def saveDataToCollection(self, collection, newDocObject, actionType):
        sessionID = self.session_manager.get()
        docs = self.m_client.find(collection, selector={'sessionID': sessionID})
        total = len(docs)
        if total > 0:
            dprint("try to replace first image in mongo, total images:", total)
            doc = docs[0]
            docID = doc["_id"]
            newDocObject["sessionID"] = sessionID
            # update, not test yet
            self.m_client.update(collection, {'_id': docID}, newDocObject, callback=self.update_callback)
        else:
            # insert
            dprint("try to to insert images")
            newDocObject["sessionID"] = sessionID
            self.m_client.insert(collection, newDocObject, callback=self.insert_callback)
            dprint("end to insert")

            #     newDocObject.sessionID = sessionID;
            #const docID = collection.insert(newDocObject);

        # save to mongo , imagecontroller
        # mongoUpsert(ImageController, { imageURL: url }, GET_IMAGE);
        # const url = `data:image/jpeg;base64,${buffer}`;
        # console.log('image url string size:', url.length);
    # fields are changed fields

    def render_received_image(self, imgString):
        dprint("render_received_image")

        imgdata = base64.b64decode(imgString)

        # NOTE: since we have tk+matplotlib for debugging, so no more saving images to files
        # dprint("try to save image")
        # currentTime = str(datetime.now())
        # dprint("currentTime:", currentTime)
        # filename = currentTime +".jpg"
        # with open(filename, 'wb') as f:
        #     f.write(imgdata)
        # dprint("end to save image")

        i = io.BytesIO(imgdata)
        i = mpimg.imread(i, format='JPG')  # from memory, binary

        if run_from_interactive():
            # plt.imshow(i, interpolation='nearest')
            imgplot = plt.imshow(i)# may be no difference
            plt.pause(0.01)
        else:
            dprint("not ipython, so do no show image after saving")
            self.debug_image_queue.put(i)
    def print_file_list(self, rootDir, files):
        print("\ncurrent folder:{}".format(rootDir))
        for file in files:
            if "type" in file:
                print("{} type:{}".format(file["name"], file["type"]))
            elif "dir" in file:
                print("{} type:{}".format(file["name"], "folder"))
            else:
                print("{} type:".format(file["name"]))
    def handleAddedOrChanged(self, collection, id, fields):
        for key, value in fields.items():
            dprint('  - FIELD {}'.format(key))
            # dprint('  - FIELD {} {}'.format(key, value))

        if collection == "users":
            dprint("grimmer users added/changed ")
        elif collection == "responses":
            dprint("grimmer responses added/changed, self_sessionID:", fields["sessionID"])

            if "pushedImage" in fields:
                # if "buffer" in fields:
                imgString = fields["buffer"]
                imageLeng = len(imgString)
                print("get image, data size in (cmd) response:", imageLeng)

                #TODO the dummy empty images should be solved in the future, but now we use it to judge connect ok
                if imageLeng > 10012:
                    # url = "data:image/jpeg;base64,"+imgString
                    # save to mongo for share screen
                    #TODO python: forget to setup controllerID. js: forget to add size
                    self.saveDataToCollection('imageviewerdb', { "imageURL": imgString, "size": len(imgString) }, GET_IMAGE)
                    #save file for testing
                    # dprint("try to save image")
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
                    #         dprint("not ipython, so do no show image after saving")

                # global numberOfImages
                self.numberOfImages += 1
                if self.numberOfImages == 2:
                    print("get dummy 2 images")
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
                    self.remote_current_folder = rootDir
                    # print("files:{};dir:{}".format(files, rootDir))
                    self.print_file_list(rootDir, files)
                    dprint("response:REQUEST_FILE_LIST end")
                    self.queue.put("get file list resp")
                elif cmd == command_SELECT_FILE_TO_OPEN:
                    print("response:SELECT_FILE_TO_OPEN")
            #2.  remove it, may not be necessary for Browser, just aligh with React JS Browser client
            self.m_client.remove('responses', {'_id': id}, callback=self.remove_callback)

        elif collection == 'imageviewerdb':
            sessionID = self.session_manager.get()
            docs = self.m_client.find(collection, selector={'sessionID': sessionID})
            total = len(docs)
            print("imagecontroller added/changed event happens, total docs:", total)
            if total > 0:
                # firstDoc = docs[0]
                for doc in docs:
                    docID = doc["_id"]
                    dprint("loop image collection, id is", docID)
                    #NOTE since meteor-python does not have Optimistic update so that we need to remove old images after getting added/changed callback
                    if docID != id:
                        print("remove one image document")
                        self.m_client.remove('imageviewerdb', {'_id': docID}, callback=self.remove_image_callback)
                        # global testimage
                        # testimage +=1
                        # if testimage ==1:
                        #     dprint("try 2nd image file")
                        #     ImageController.selectFileToOpen2(client)
                        #
                        # doc["comments"] = "apple"
                        # for testing client.update('imageviewerdb', {'_id': docID}, {"name": "ggg"}, callback=update_callback)
                        # for testing
                        # client.update('imageviewerdb', {'_id': docID}, doc, callback=update_callback)
                    else:
                        dprint("not remove it")
                        print("image size in collection:", len(doc["imageURL"]))
                        self.render_received_image(doc["imageURL"])

                        # delete previous images

    #TODO commmand response need to be deleted.
    def added(self, collection, id, fields):
        dprint('* ADDED {} {}'.format(collection, id))
        self.handleAddedOrChanged(collection, id, fields)
        dprint('end added')


    #  ADDED users vo5Eb7cG94waZmiGY
    #   - FIELD username grimmer4

        # query the data each time something has been added to
        # a collection to see the data `grow`
        # all_lists = client.find('lists', selector={})
        # dprint('Lists: {}'.format(all_lists))
        # dprint('Num lists: {}'.format(len(all_lists)))

        # if collection == 'list' you could subscribe to the list here
        # with something like
        # client.subscribe('todos', id)
        # all_todos = client.find('todos', selector={})
        # dprint 'Todos: {}'.format(all_todos)

        # all_lists = client.find('tasks', selector={})
        # dprint('Tasks: {}'.format(all_lists))
        # dprint('Num lists: {}'.format(len(all_lists)))

    def changed(self, collection, id, fields, cleared):
        dprint('CHANGED !!!: {} {}'.format(collection, id))
        handleAddedOrChanged(collection, id, fields) # only take effect when JS changes rendered image

        # all_lists = client.find('tasks', selector={})
        # dprint('Tasks: {}'.format(all_lists))
        # dprint('Num lists: {}'.format(len(all_lists)))
        dprint('end changed')



        # conf.set('ddp', 'token', data['token'])
        # conf.update()

    def subscription_response_callback(self, error):
        if error:
            dprint("sub fail")
            dprint(error)
        dprint("sub resp ok")

    def subscription_image_callback(self, error):
        if error:
            dprint("sub2 fail")
            dprint(error)
        dprint("sub image ok2")
        if self.use_other_session == False:
            ImageController.sendRegiserView(self.session_manager.get(), self.m_client)

    def setup_subscription(self):
        dprint("get:", self.session_manager.get())

        if self.use_other_session == False:
            self.m_client.subscribe('commandResponse', [self.session_manager.get()], callback=self.subscription_response_callback)

        self.m_client.subscribe('imageviewerdb', [self.session_manager.get()], callback=self.subscription_image_callback)
    def getSession_callback(self, error, result):
        if error:
            dprint("getSession_callback error")
            dprint(error)
            return
        print("in getSession_callback, sessionID:", result)
        if self.use_other_session == False:
            self.session_manager.set(result)
        # subscribe response
        # subscribe imageController
        # observe response, imageController
        self.setup_subscription()

    def getSession(self):
        dprint("try getSession")
        dprint("setup subscription callback")

        # empty params, so []
        self.m_client.call(getSessionCmd, [], self.getSession_callback)

    def connected(self):
        dprint('* CONNECTED')
        # all_lists = client.find('tasks', selector={})
        # dprint('Tasks: {}'.format(all_lists))
        # dprint('Num lists: {}'.format(len(all_lists)))
        if self.use_other_session == False:
            dprint('setup subscribe collection in session callback')
            self.getSession()
        else:
            self.setup_subscription()
            self.queue.put(connect_response)
        print('connected, try login')
        self.m_client.login(self.user, self.password)

    def removed(self, collection, id):
        dprint('* REMOVED {} {}'.format(collection, id))

    def on_logged_in(self, data):
        print('LOGGIN IN', data)

print("import client ok")
# (sort of) hacky way to keep the client alive
# ctrl + c to kill the script
# while True:
#     try:
#         time.sleep(5)
#     except KeyboardInterrupt:
#         break
