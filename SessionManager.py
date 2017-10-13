
print("load import SessionManager, sessionid")

selfSessionID = None
otherSessionID = None #"B6bugxuJGmwcX3FPY" # for testing

# can be replaced by get_suitable_session totally
def get():
    print("load sessionid", selfSessionID)
    if otherSessionID != None:
        return otherSessionID
    return selfSessionID

def set(sessionID):
    global selfSessionID
    print("setupt sessionid")
    selfSessionID = sessionID

def get_suitable_session():
    if otherSessionID != None:
        return otherSessionID
    return selfSessionID

def use_other_ession(sessionID):
    otherSessionID = sessionID
