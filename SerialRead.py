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


def data_management(port_baud, aosdv_type, shared_data_supervisor, shared_data_time, shared_data_yaw, shared_data_pitch,
                    shared_data_roll, shared_data_quatW, shared_data_quatX, shared_data_quatY, shared_data_quatZ,
                    shared_data_temp1, shared_data_temp2, shared_data_emf1, shared_data_emf2):
    data_time = 0
    length_data = 117

    if aosdv_type["local"] or aosdv_type["streamer"] or aosdv_type["reader"]:

        if aosdv_type["reader"] or aosdv_type["streamer"]:
            Client.initialize()
            if not Client.send_data(aosdv_type[
                                        "streamer"]):  # if data could not be sent to the server then it means server is not available so quit program
                quit()

        while True:

            while shared_data_supervisor[0] == 'stop':
                time.sleep(1)

            count = 1

            while shared_data_supervisor[0] == 'clear':
                if count == 1:
                    shared_data_time[:] = []

                    shared_data_yaw[:] = []
                    shared_data_pitch[:] = []
                    shared_data_roll[:] = []

                    shared_data_quatW[:] = []
                    shared_data_quatX[:] = []
                    shared_data_quatY[:] = []
                    shared_data_quatZ[:] = []

                    shared_data_temp1[:] = []
                    shared_data_temp2[:] = []

                    shared_data_emf1[:] = []
                    shared_data_emf2[:] = []

                    count = 2

                time.sleep(1)

            while shared_data_supervisor[0] == 'start':

                if aosdv_type["reader"]:
                    data = Client.receive_data(length_data)
                    if data == -1:  # it means server is not available
                        quit()
                    elif data != 0:  # it means data is valid
                        shared_data_time.append(data[0])

                        shared_data_yaw.append(data[1])
                        shared_data_pitch.append(data[2])
                        shared_data_roll.append(data[3])

                        shared_data_quatW.append(data[4])
                        shared_data_quatX.append(data[5])
                        shared_data_quatY.append(data[6])
                        shared_data_quatZ.append(data[7])

                        shared_data_temp1.append(data[8])
                        shared_data_temp2.append(data[9])

                        shared_data_emf1.append(data[10])
                        shared_data_emf2.append(data[11])

                    time.sleep(0.5)


                else:
                    data_yaw = random.randint(-90, 90) * random.random()
                    data_pitch = random.randint(-90, 90) * random.random()
                    data_roll = random.randint(-90, 90) * random.random()

                    data_quatW = random.randint(-1, 1) * random.random()
                    data_quatX = random.randint(-1, 1) * random.random()
                    data_quatY = random.randint(-1, 1) * random.random()
                    data_quatZ = random.randint(-1, 1) * random.random()

                    data_temp1 = random.randint(150, 160) * random.random()
                    data_temp2 = random.randint(-50, 60) * random.random()

                    data_emf1 = random.randint(12, 13) * random.random()
                    data_emf2 = random.randint(12, 13) * random.random()

                    shared_data_time.append(data_time)
                    shared_data_yaw.append(data_yaw)
                    shared_data_pitch.append(data_pitch)
                    shared_data_roll.append(data_roll)

                    shared_data_quatW.append(data_quatW)
                    shared_data_quatX.append(data_quatX)
                    shared_data_quatY.append(data_quatY)
                    shared_data_quatZ.append(data_quatZ)

                    shared_data_temp1.append(data_temp1)
                    shared_data_temp2.append(data_temp2)

                    shared_data_emf1.append(data_emf1)
                    shared_data_emf2.append(data_emf2)

                    if aosdv_type["streamer"]:
                        data = [data_time, data_yaw, data_pitch, data_roll, data_quatW, data_quatX, data_quatY,
                                data_quatZ, data_temp1, data_temp2, data_emf1, data_emf2]
                        if not Client.send_data(
                                data):  # if data could not be sent to the server then it means server is not available so quit program
                            quit()

                    data_time = data_time + 1

                    time.sleep(0.5)

    if aosdv_type["recorded"]:

        DBMS.dbms.initialize()

        data = DBMS.dbms.read_from_database()

        DateOfCreation = data[0][0][0]
        Description = data[0][0][1]

        print("ABOUT DATA!!!!!")
        print("Date Of Creation:", DateOfCreation)
        print("Description:", Description)


        for datum in data[1]:
            shared_data_time.append(datum[0])

            shared_data_yaw.append(datum[1])
            shared_data_pitch.append(datum[2])
            shared_data_roll.append(datum[3])

            shared_data_quatW.append(datum[4])
            shared_data_quatX.append(datum[5])
            shared_data_quatY.append(datum[6])
            shared_data_quatZ.append(datum[7])

            shared_data_temp1.append(datum[8])
            shared_data_temp2.append(datum[9])

            shared_data_emf1.append(datum[10])
            shared_data_emf2.append(datum[11])