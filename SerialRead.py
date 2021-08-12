import time
import random

import DBMS

import Client

import ast

def getport_baud():
    file = open("config/config.txt", "r")
    contents = file.read()
    dictionary = ast.literal_eval(contents)
    port_baud = dictionary["Portname"] + ',' + dictionary["Baudrate"]
    file.close()

    return port_baud

def data_management(port_baud, aosdv_type, shared_data_supervisor, shared_data_time, shared_data_head, shared_data_pitch, shared_data_roll):
    data_time = 0
    length_data = 52

    if aosdv_type["local"] or aosdv_type["streamer"] or aosdv_type["reader"]:

        if aosdv_type["reader"] or aosdv_type["streamer"]:
            Client.initialize()
            if not Client.send_data(aosdv_type["streamer"]):  # if data could not be sent to the server then it means server is not available so quit program
                quit()


        while True:

            while shared_data_supervisor[0] == 'stop':
                time.sleep(1)

            count = 1

            while shared_data_supervisor[0] == 'clear':
                print("clear")
                if count == 1:
                    shared_data_time[:] = []
                    shared_data_head[:] = []
                    shared_data_pitch[:] = []
                    shared_data_roll[:] = []

                    count = 2

                time.sleep(1)

            while shared_data_supervisor[0] == 'start':

                if aosdv_type["reader"]:
                    print("reader ho timi")
                    data = Client.receive_data(length_data)
                    if data == -1:  # it means server is not available
                        quit()
                    elif data != 0:  # it means data is valid
                            shared_data_time.append(data[0])
                            shared_data_head.append(data[1])
                            shared_data_pitch.append(data[2])
                            shared_data_roll.append(data[3])
                    time.sleep(0.1)

                else:
                    data_head = random.randint(-90, 90)
                    data_pitch = random.randint(-90, 90)
                    data_roll = random.randint(-90, 90)

                    shared_data_time.append(data_time)
                    shared_data_head.append(data_head)
                    shared_data_pitch.append(data_pitch)
                    shared_data_roll.append(data_roll)



                    if aosdv_type["streamer"]:
                        data = [data_time, data_head, data_pitch, data_roll]
                        if not Client.send_data(data):  # if data could not be sent to the server then it means server is not available so quit program
                            quit()

                    data_time = data_time + 1

                    time.sleep(0.5)



    if aosdv_type["recorded"]:
        print("recorded")

        DBMS.dbms.initialize()

        datum = DBMS.dbms.read_from_database()
        for data in datum:
            shared_data_time.append(data[0])
            shared_data_head.append(data[1])
            shared_data_pitch.append(data[2])
            shared_data_roll.append(data[3])
