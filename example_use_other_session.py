
# import cartaclient as client
import sessionmanager as SessionManager

from client import Client
# import client

def main():
    print("start cartaclient + share session example")
    SessionManager.use_other_ession("XnfRTJe3nAdDdxZaq")
    c=Client()
    c.start_connection()

if __name__ == '__main__':
    main()
    # (sort of) hacky way to keep the client alive
    # ctrl + c to kill the script
    # while True:
    #     try:
    #         time.sleep(5)
    #     except KeyboardInterrupt:
    #         break
