
# import cartaclient as client

from client import Client
# import client

def main():
    print("start cartaclient example")
    c=Client()
    c.start_connection()
    c.requset_file_list()
    c.request_file_show("aJ.fits")

if __name__ == '__main__':
    main()
    # (sort of) hacky way to keep the client alive
    # ctrl + c to kill the script
    # while True:
    #     try:
    #         time.sleep(5)
    #     except KeyboardInterrupt:
    #         break
