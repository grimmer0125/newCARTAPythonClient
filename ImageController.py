#import SessionManager
import sessionmanager as SessionManager

import time

from os.path import expanduser


controllerID = None

command_REGISTER_IMAGEVIEWER = '/CartaObjects/ViewManager:registerView'
command_SELECT_FILE_TO_OPEN = '/CartaObjects/ViewManager:dataLoaded'

sendCmd = 'sendCommand'
setSizeCmd = 'setupViewSize'

def setSizeCallback(error, result) :
    if error:
        print(error)
        return
    print("in setSizeCallback_callback")
    print(result)

def parseReigsterViewResp(client, data):
    print("parseReigsterViewResp, try to send setupt size")
    global controllerID
    controllerID = data
    viewName = controllerID+"/view"
    width = 637 #// TODO same as the experimental setting in ImageViewer, change later
    height = 677
    client.call(setSizeCmd, [viewName, width, height,], setSizeCallback)

    # Meteor.call('setupViewSize', viewName, width, height, (error, result) => {
    #     console.log('get setupViewSize dummy result:', result);
    # });

def selectFileToOpen(client, file):
    # time.sleep(10) # 10 for testing sharing session between python and browser

    home = expanduser("~")
    # print(home)
    path = home + "/CARTA/Images/" + file

    # controllerID = state.imageController.controllerID;
    parameter = "id:"+controllerID+",data:"+path
    print("query:", parameter)
    # console.log('inject file parameter, become:', parameter);
    #
    # Meteor.call('sendCommand', Commands.SELECT_FILE_TO_OPEN, parameter, SessionManager.get_suitable_session(), (error, result) => {
    #   console.log('get select file result:', result);
    # });
    def selectFile_callback(error, result):
        if error:
            print(error)
            return
        print("in selectFile_callback")
        print(result)

    client.call(sendCmd, [command_SELECT_FILE_TO_OPEN, parameter, SessionManager.get_suitable_session()], selectFile_callback)

def selectFileToOpen2(client):
    time.sleep(10)

    path = "/Users/grimmer/CARTA/Images/a-verysmall.fits"
    # controllerID = state.imageController.controllerID;
    parameter = "id:"+controllerID+",data:"+path
    print("query:", parameter)
    # console.log('inject file parameter, become:', parameter);
    #
    # Meteor.call('sendCommand', Commands.SELECT_FILE_TO_OPEN, parameter, SessionManager.get_suitable_session(), (error, result) => {
    #   console.log('get select file result:', result);
    # });
    def selectFile_callback(error, result):
        if error:
            print(error)
            return
        print("in selectFile_callback")
        print(result)

    client.call(sendCmd, [command_SELECT_FILE_TO_OPEN, parameter, SessionManager.get_suitable_session()], selectFile_callback)

def sendRegiserView(client):
    print("sendRegiserView")
    # cmd = '/CartaObjects/ViewManager:registerView'
    # const cmd = Commands.REGISTER_IMAGEVIEWER; // '/CartaObjects/ViewManager:registerView';
    params = 'pluginId:ImageViewer,index:0'
    # // this.BASE_PATH = this.SEP + this.CARTA + this.SEP;
    # // return `${this.BASE_PATH + this.VIEW_MANAGER + this.SEP_COMMAND}registerView`;

    def registerview_callback(error, result):
        if error:
            print(error)
            return
        print("in registerview_callback")
        print(result)

    client.call(sendCmd, [command_REGISTER_IMAGEVIEWER, params, SessionManager.get_suitable_session()], registerview_callback)
