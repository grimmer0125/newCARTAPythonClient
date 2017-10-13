
print("load import SessionManager, sessionid")

selfSessionID = None
otherSessionID = None #"B6bugxuJGmwcX3FPY" # for testing

# can be replaced by get_suitable_session totally
def get():
    print("get session")
    if otherSessionID != None:
        print("load other sessionid", otherSessionID)
        return otherSessionID
    else:
        print("load self sessionid", selfSessionID)
    return selfSessionID

def set(sessionID):
    global selfSessionID
    print("setupt sessionid")
    selfSessionID = sessionID

# def get_suitable_session():
#     print("get suitable session")
#     if otherSessionID != None:
#         print("load other sessionid", otherSessionID)
#         return otherSessionID
#     print("load self sessionid", selfSessionID)
#     return selfSessionID

def use_other_session(sessionID):
    global otherSessionID
    otherSessionID = sessionID
