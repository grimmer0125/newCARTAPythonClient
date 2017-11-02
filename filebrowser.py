from helper import *

import sessionmanager as SessionManager

sendCmd = 'sendCommand'
command_REQUEST_FILE_LIST = '/CartaObjects/DataLoader:getData'

def queryServerFileList(session, client):
    dprint("queryServerFileList")
    # cmd = '/CartaObjects/ViewManager:registerView'
    # const cmd = Commands.REGISTER_IMAGEVIEWER; // '/CartaObjects/ViewManager:registerView';
    params = 'path:'
    # // this.BASE_PATH = this.SEP + this.CARTA + this.SEP;
    # // return `${this.BASE_PATH + this.VIEW_MANAGER + this.SEP_COMMAND}registerView`;

    def query_file_list_callback(error, result):
        if error:
            dprint(error)
            return
        dprint("in query_file_list_callback")
        dprint(result)

    client.call(sendCmd, [command_REQUEST_FILE_LIST, params, session], query_file_list_callback)
