
print("load import SessionManager, sessionid")

selfSessionID = None
otherSessionID = None #"B6bugxuJGmwcX3FPY" # for testing

# can be replaced by getSuitableSession totally 
def get():
    print("load sessionid", selfSessionID)
    if otherSessionID != None:
        return otherSessionID
    return selfSessionID

def set(sessionID):
    global selfSessionID
    print("setupt sessionid")
    selfSessionID = sessionID

def getSuitableSession():
    if otherSessionID != None:
        return otherSessionID
    return selfSessionID
