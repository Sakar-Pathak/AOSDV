import socket
import sys
import pickle

import ast



client = None


# Create connection with the server
def initialize():
    global client


    file = open("config/config.txt", "r")
    contents = file.read()
    dictionary = ast.literal_eval(contents)
    host = dictionary["Host"]
    port = dictionary["Port"]
    file.close()


    for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
        # af - address family, sa - server address
        af, socktype, proto, canonname, sa = res

        try:
            client = socket.socket(af, socktype, proto)
        except OSError as msg:
            print(msg)
            client = None
            continue

        try:
            client.connect(sa)
        except OSError as msg:
            print(msg)
            client.close()
            client = None
            continue

        break



    if client is None:
        print('could not connnect to the server')
        sys.exit(1)



# This function asks the client if he wants to stream data or read data
def SON():
    son = int(input("please enter:\n1 --> if you are a streamer\n2 --> if you are a reader\n"))

    if son == 1:
        son = True

    elif son == 2:
        son = False


    return son


# function to send data to the server
def send_data(data):
    data = pickle.dumps(data)
    try:
        client.send(data)
        return True
    except:
        client.close()
        return False


# function to receive data of certain length from the server
def receive_data(length_data):
    try:
        temp = client.recv(length_data)
    except:                                 # if server is not available it closes connection with the server
        client.close()
        return -1

    try:
        data = pickle.loads(temp)       # if the data is loaded by pickle then it means it is valid data
        return data
    except:
        return 0