# -*- coding: utf-8 -*-
#from threading import Thread
from threading import Thread, Lock


import sys
is_py2 = sys.version[0] == '2'
if is_py2:
    print("use python 2")
    # reload(sys)  # 2
    # sys.setdefaultencoding('utf-8')
    import Queue as queue
    # from Tkinter import *
else:
    print("use python 3")
    import queue as queue

from helper import *
from sessionmanager import SessionManager
sendCmd = 'sendCommand'
# https://gist.github.com/pazdera/1098129


class ApiService:
    # Here will be the instance stored.
    __instance = None

    @staticmethod
    def instance():
        """ Static access method. """
        if ApiService.__instance == None:
            ApiService.__instance = ApiService()
        return ApiService.__instance

    def set_client(self, client):
        self.client = client

    def block_for_user_callback(self):
        print("block_for_user_callback")
        data = self.sync_resp_queue.get()
        print("resp:{}".format(data))
        return data

    # network thread
    def consume_response(self, resp):
        print("get resp".format(resp))
        #cmd = resp
        cmd = resp['cmd']
        parameter = resp['parameter']
        target = cmd + parameter
        self.mutex.acquire()

        match = None
        for index, callback in enumerate(self.callbacks):
            identifier = callback['id']
            if identifier == target:
                print("got the target")
                match = callback
                self.callbacks.pop(index)
                break

            # print("President {}: {}".format(num, name))
        # for callback in self.callbacks:
        #     identifier = callback['id']
        #     if identifier == target:
        #         print("got the target")
        #
        #         break

        self.mutex.release()

        if match != None:
            built_callback = callback['built_callback']
            built_callback(resp)
            user_callback = callback['user_callback']
            data = resp["data"]
            if user_callback == None:
                self.sync_resp_queue.put(data)
                print("after unlock ")
            elif user_callback != "":
                user_callback(data)

    # def dummy_user_callback(self):
    #     print("it is a dummy user_callback")

    def send_command_callback(self, error, result):
        if error:
            print(error)
        return
        print(result)
    # queryServerFileList
    # user thread
    ## Note: 無法開兩個thread, 使用同一個client, 發同步類型的commands, 因為sync_resp_queue無法區別
    #TODO, add error with result, now it only handles result
    def send_command(self, cmd, parameter, built_callback= None, user_callback=""):
        # 有built_callback就先處理它. 然後有user_callback就async,  沒有就直接return result
        # 沒有built_callback就建一個dummmy, 然後裡面再callback user_callback
        # 沒有user_callback就要把self.sync_resp_queue.put
        # 也有可能都沒有
        print("send command".format("cmd"))
        identifier = cmd + parameter
                #const id = cmd + parameter;

        # cmd_dict = {'if_async': if_async, 'callback': callback}
        cmd_dict = {'id': identifier, 'built_callback': built_callback, 'user_callback': user_callback}

        self.mutex.acquire()
        self.callbacks.append(cmd_dict)
        self.mutex.release()
        self.client.call(sendCmd, [cmd, parameter, SessionManager.instance().get_session()], self.send_command_callback)
        if user_callback == None:
            data = self.block_for_user_callback()
            return data
        else:
            print("async send command !!!!!")

    def setup_size_callback(self):
        print('setup_size_callback')

    def setup_size(self, view_name, width, height):
        setSizeCmd = 'setupViewSize'
        self.client.call(setSizeCmd, [view_name, width, height], self.setup_size_callback)

    def __init__(self):
        """ Virtually private constructor. """
        if ApiService.__instance != None:
            raise Exception("This class is a singleton!")
        # else:
        #     ApiService.__instance = self
        self.callbacks = []
        self.mutex = Lock()
        self.sync_resp_queue = queue.Queue()


# FileBrowser.queryServerFileList(self.session_manager.get(), self.m_client)

# JavaScript's version
# api.instance().sendCommand(cmd, arg, (resp) => {
#       // console.log('get register animator result:', resp);
#       mongoUpsert(AnimatorDB, { animatorID: resp.data }, `Resp_${cmd}`);
#     });

# s = Singleton() # Ok
# #Singleton() # will raise exception
# print s
