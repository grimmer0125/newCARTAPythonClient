from helper import *

#print("load import SessionManager, sessionid")

class SessionManager():
    def __init__(self):
        self.otherSessionID = None #"B6bugxuJGmwcX3FPY" # for testing
        self.selfSessionID = None

    def use_other_session(self, sessionID):
        # global otherSessionID
        self.otherSessionID = sessionID

    def set(self, sessionID):
        # global selfSessionID
        dprint("setup sessionid")
        self.selfSessionID = sessionID

    # can be replaced by get_suitable_session totally
    def get(self):
        dprint("get session")
        if self.otherSessionID != None:
            dprint("load other sessionid", self.otherSessionID)
            return self.otherSessionID
        else:
            dprint("load self sessionid", self.selfSessionID)
        return self.selfSessionID

# def get_suitable_session():
#     print("get suitable session")
#     if otherSessionID != None:
#         print("load other sessionid", otherSessionID)
#         return otherSessionID
#     print("load self sessionid", selfSessionID)
#     return selfSessionID
