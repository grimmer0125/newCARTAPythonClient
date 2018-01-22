from helper import *

# import sessionmanager as SessionManager
from apiService import ApiService

import commands as Commands

# sendCmd = 'sendCommand'
# command_REQUEST_FILE_LIST = '/CartaObjects/DataLoader:getData'

# TODO add some method to save data in mongo, not member.
# This is for share screen
class FileManager():
    def __init__(self):
        self.remote_current_folder = None

        # self.session_manager = session
        # self.client = client

    # def queryServerFileList(self, session, client):
        # cmd = '/CartaObjects/ViewManager:registerView'
        # const cmd = Commands.REGISTER_IMAGEVIEWER; // '/CartaObjects/ViewManager:registerView';
        # // this.BASE_PATH = this.SEP + this.CARTA + this.SEP;
        # // return `${this.BASE_PATH + this.VIEW_MANAGER + this.SEP_COMMAND}registerView`;

    def print_file_list(self, rootDir, files):
        print("\ncurrent folder:{}".format(rootDir))
        for file in files:
            if "type" in file:
                print("{} type:{}".format(file["name"], file["type"]))
            elif "dir" in file:
                print("{} type:{}".format(file["name"], "folder"))
            else:
                print("{} type:".format(file["name"]))

    #TODO change to self, error, result
    def query_file_list_callback(self, result):
        # if error:
        #     dprint(error)
        #     return
        dprint("in query_file_list_callback")
        dprint(result)
        data = result["data"]
        files = data["dir"]
        rootDir= data["name"]
        self.remote_current_folder = rootDir
        self.print_file_list(rootDir, files)
        dprint("response:REQUEST_FILE_LIST end")

    def request_file_list(self):

        # TODO do not pass session or client directly to this class, later.
        # use the way newMeteorCARTA uses, apiService
        # self.queryServerFileList(self.session_manager.get(), self.client)
        dprint("queryServerFileList")
        params = 'path:'

        ApiService.instance().send_command(Commands.REQUEST_FILE_LIST, params, self.query_file_list_callback)
        print('after send request file list')
        # self.client.call(sendCmd, [Commands.REQUEST_FILE_LIST, params, session.get()], query_file_list_callback)
