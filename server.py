import socket
import sys

import threading
from asyncio import threads

from self import *
from time import sleep
from tcp_server import *


def main():
    #declaring my server
    my_server = tcp_Server()
    #declaring socket details
    mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #declaring server address and port number
    server_address = ('192.168.56.1', 6262)
    print('starting up on {} port {}'.format(*server_address))
    # binding socket to the port 6262
    mysock.bind(server_address)

    #listening to the incoming connections(10)
    mysock.listen(10)

    #communicating with the server
    my_server.Communication_With_Server(mysock)

#This is just used for the main
if __name__ == "__main__":
    main()
