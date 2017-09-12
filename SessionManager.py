
print("load import SessionManager, sessionid")

selfSessionID = None
otherSessionID = None

def get():
    print("load sessionid", selfSessionID)
    return selfSessionID

def set(sessionID):
    global selfSessionID
    print("setupt sessionid")
    selfSessionID = sessionID

def getSuitableSession():
    return selfSessionID
