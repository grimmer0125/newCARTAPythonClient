import SessionManager

controllerID = None

command_REGISTER_IMAGEVIEWER = '/CartaObjects/ViewManager:registerView'
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

    client.call(sendCmd, [command_REGISTER_IMAGEVIEWER, params, SessionManager.getSuitableSession()], registerview_callback)
