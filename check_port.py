# Checking UDP port; for TCP: socket.socket(socket.AF_INET, socket.SOCK_STREAM)

import socket
from contextlib import closing

host = ''
port = 53


def check_socket(host, port):
    try:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
            sock.bind((host, port))
            if sock.connect_ex((host, port)) == 0:
                print ("Port is open")
    except socket.error as msg:
        print ('Bind failed. Error Code : ' +
               str(msg[0]) + '. Message: ' + msg[1])


check_socket(host, port)
