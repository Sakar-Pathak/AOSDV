import socket
from _thread import *
import pickle
import time

number_of_clients = 4   # 3 here means that 3 connections are kept waiting if the server is busy and if a 4th socket trys to connect then the connection is refused.
server_name = ''        # accepts both ipv4 and ipv6
port_number = 50007


# Create Server
address = (server_name, port_number)
try:
    myserver = socket.create_server(address, family = socket.AF_INET6, dualstack_ipv6=True, backlog=False)

except socket.error as e:
    print(str(e))

myserver.listen(number_of_clients)




# function to send data to the client
def send_data(conn, data):
    temp = pickle.dumps(data)

    try:
        conn.send(temp)
    except:
        conn.close()
        return -1

    return 1



# function to receive data of certain length from the client
def receive_data(conn, length_data):
    try:
        temp = conn.recv(length_data)
    except:
        conn.close()
        return -1


    data = pickle.loads(temp)

    return data





# SON - Streamer Or Not
# This function checks if the client is streamer or not and calls the required function
def SON(conn):
    global streamer_conn
    length_son = 4  # son is a boolean whose pickled length is 4

    son = receive_data(conn, length_son)


    if son == True:
        start_new_thread(client_streamer, (conn,))

    elif son == False:
        start_new_thread(client_reader, (conn,))

    else:
        return 0


data = None                         # this data variable stores the data read from the streamer client to send it to the reader clients
length_data = 117                    # length of data sent by the streamer client
new_data = False                    # True if new_data is available else false
is_streamer_available = False       # True when the streamer is connected with the server else false


# This function grabs the new data from streamer and stores it in data variable
def client_streamer(conn):
    global data
    global new_data
    global is_streamer_available
    is_streamer_available = True

    while True:
        try:
            data = conn.recv(length_data)   # TODO:  when client exits at this step then server keeps waiting for the client who have already disconnected
            new_data = True
        except:                             # when streamer gets disconnected
            conn.close()                    # close the connection with the streamer
            print("connection with streamer closed")
            is_streamer_available = False
            break


# This function sends the data which was received from the streamer and stored in data variable to all the reader clients
# Same data should not be sent multiple times
def client_reader(conn):
    global new_data

    while True:
        if new_data:            # if new data is available then only send the data to the reading client
            try:
                conn.send(data)
                new_data = False
            except:                # if new reader is not available then close the connection
                conn.close()
                print("connection with reader closed")
                break

        elif not is_streamer_available:     # if streamer is not available then check if reader is also available or not. If not close the connection with the reader

            try:
                msg = "are you there?"
                conn.send(bytes(msg, "utf-8"))  # sending with utf-8 so that the pickle couldnot load that and so it can be discarded in the reader side
            except:
                conn.close()
                print("connection with reader closed")
                break

        time.sleep(0.5)





while True:
    try:
        conn, addr = myserver.accept()
    except:
        conn.close()

    print("connected to: ", addr)

    start_new_thread(SON, (conn,))  # calling the SON function which handles streamers and readers
