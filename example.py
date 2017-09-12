# https://github.com/hharnisc/python-meteor
import time

from lib.meteor.MeteorClient import MeteorClient
import SessionManager
import ImageController

client = MeteorClient('ws://127.0.0.1:3000/websocket')

####  grimmer's experiment
getSessionCmd = "getSessionId"
sefSessionID = None
command_REGISTER_IMAGEVIEWER = '/CartaObjects/ViewManager:registerView'
command_SELECT_FILE_TO_OPEN = '/CartaObjects/ViewManager:dataLoaded'
controllerID = None

def subscribed(subscription):
    print('* SUBSCRIBED {}'.format(subscription))

def unsubscribed(subscription):
    print('* UNSUBSCRIBED {}'.format(subscription))

def remove_callback(error, data):
    print("in remove_callback")
    if error:
        print(error)
        return
    print(data)

def handleAddedOrChanged(collection, id, fields):
    for key, value in fields.items():
        print('  - FIELD {} {}'.format(key, value))

    if collection == "users":
        print("grimmer users added ")
    elif collection == "responses":
        print("grimmer responses added, session:", fields["sessionID"])

        cmd = fields["cmd"]

        #1. TODO handle it
        if cmd == command_REGISTER_IMAGEVIEWER:
            print("response:REGISTER_IMAGEVIEWER")
            data = fields["data"] # save controllerID to use
            ImageController.parseReigsterViewResp(client, data)

        elif cmd == command_SELECT_FILE_TO_OPEN:
            print("response:SELECT_FILE_TO_OPEN, get image !!!!")
            image = fields["buffer"]
            print("image data size:", len(image))

        #2.  remove it, may not be necessary for Browser, just alight with React JS Browser client
        client.remove('responses', {'_id': id}, callback=remove_callback)

    elif collection == "imagecontroller":
        print("grimmer imagecontroller added")

#TODO commmand response need to be deleted.
def added(collection, id, fields):
    print('* ADDED {} {}'.format(collection, id))
    handleAddedOrChanged(collection, id, fields)
    print('end added')

        # 要把response刪掉嗎? 之前是下一次進來會用到舊的

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

def changed(collection, id, fields, cleared):
    print('* CHANGED {} {}'.format(collection, id))
    handleAddedOrChanged(collection, id, fields)

    # all_lists = client.find('tasks', selector={})
    # print('Tasks: {}'.format(all_lists))
    # print('Num lists: {}'.format(len(all_lists)))
    print('end changed')



    # conf.set('ddp', 'token', data['token'])
    # conf.update()

def subscription_response_callback(error):
    if error:
        print("sub fail")
        print(error)
    print("sub resp ok")

def subscription_image_callback(error):
    if error:
        print("sub2 fail")
        print(error)
    print("sub image ok2")
    ImageController.sendRegiserView(client)

def getSession_callback(error, result):
    if error:
        print(error)
        return
    print("in getSession_callback")
    print(result)
    SessionManager.set(result)
    print("get:", SessionManager.get())
    client.subscribe('commandResponse', [SessionManager.get()], callback=subscription_response_callback)
    client.subscribe('imagecontroller', [SessionManager.get()], callback=subscription_image_callback)
    # subscribe response
    # subscribe imageController
    # observe response, imageController

def getSession():
    print("try getSession")
    # empty params, so []
    client.call(getSessionCmd, [], getSession_callback)

def connected():
    print('* CONNECTED')
    all_lists = client.find('tasks', selector={})
    print('Tasks: {}'.format(all_lists))
    print('Num lists: {}'.format(len(all_lists)))
    print('end connected, try login')
    client.login('grimmer4', "123456")
    print('setup collection')

def removed(collection, id):
    print('* REMOVED {} {}'.format(collection, id))

def on_logged_in(data):
    print('LOGGIN IN', data)

client.on('removed', removed)

client.on('changed', changed)
client.on('subscribed', subscribed)
client.on('unsubscribed', unsubscribed)
client.on('added', added)
client.on('connected', connected)
client.on('logged_in', on_logged_in)

client.connect()

# client.subscribe('publicLists')
getSession()
# client.subscribe('tasks')


# (sort of) hacky way to keep the client alive
# ctrl + c to kill the script
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break

# client.unsubscribe('publicLists')


# todo:
#     一開始 Meteor.call('getSessionId', (err, sessionID) => {
#         存自己sessionid, print
#         1 subscribe, command response 2 observe respone
#         2, 3 其他兩個, filebrowser , 跟 imagecontroller

# *跳過filebrowser的file list階段好了 -> 不知道如何呈現
# image部份:
#     1. 送 REGISTER_IMAGEVIEWER 得到 controller id
#     2. 得到後set size
# 之後就會得到command response: image的資料 !!!!

# cmdAsyncList 真的是非blocking????
