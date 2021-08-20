import mysql.connector

import ast

class Dbms():
    def initialize(self):

        file = open("config/config.txt", "r")
        contents = file.read()
        dictionary = ast.literal_eval(contents)
        host = dictionary["Host"]
        user = dictionary["User"]
        password = dictionary["Password"]
        database = dictionary["Database"]
        file.close()

        try:
            self.connection = mysql.connector.connect(host = host,
                                                      user = user,
                                                      password = password,
                                                      database = database,
                                                      auth_plugin='mysql_native_password')
            self.cursor = self.connection.cursor

        except mysql.connector.Error as error:
            print("Failed to connect {}".format(error), "\n")

        finally:
            if self.connection.is_connected():
                print("Connection Established", "\n")



    def save_to_database(self, data):
        try:

            cursor = self.connection.cursor()

            mysql_insert_streamer_query = """INSERT INTO streamer (CreatedBy, DataName, Description)
                                              VALUES (%s, %s, %s) """


            cursor.executemany(mysql_insert_streamer_query, data[0])


            mysql_insert_ypr_query = """INSERT INTO ypr (CreatedBy, DataName, Time, Yaw, Pitch, Roll)
                                              VALUES (%s, %s, %s, %s, %s, %s) """
            mysql_insert_quaternion_query = """INSERT INTO quaternion (CreatedBy, DataName, Time, QuatW, QuatX, QuatY, QuatZ)
                                              VALUES (%s, %s, %s, %s, %s, %s, %s) """
            mysql_insert_temperature_query = """INSERT INTO temperature (CreatedBy, DataName, Time, Temp1, Temp2)
                                              VALUES (%s, %s, %s, %s, %s) """
            mysql_insert_solar_voltage_query = """INSERT INTO solar_voltage (CreatedBy, DataName, Time, Emf1, Emf2)
                                              VALUES (%s, %s, %s, %s, %s) """

            cursor.executemany(mysql_insert_ypr_query, data[1])
            cursor.executemany(mysql_insert_quaternion_query, data[2])
            cursor.executemany(mysql_insert_temperature_query, data[3])
            cursor.executemany(mysql_insert_solar_voltage_query, data[4])
            self.connection.commit()

            return True


        except mysql.connector.Error as error:
            print("Error saving to database {}".format(error))
            return False




    def read_from_database(self):
        cursor = self.connection.cursor()


        mysql_read_date_description_query = """SELECT DateOfCreation, Description 
                                                FROM streamer
                                                WHERE CreatedBy = %s AND DataName = %s"""

        mysql_read_data_query = """SELECT x.Time, x.Yaw, x.Pitch, x.Roll, x.QuatW, x.QuatX, x.QuatY, x.QuatZ, x.Temp1, x.Temp2, x.Emf1, x.Emf2
                                    FROM 
                                    (SELECT *
                                    FROM ypr
                                    NATURAL INNER JOIN quaternion 
                                    NATURAL INNER JOIN temperature
                                    NATURAL INNER JOIN solar_voltage) as x
                                    WHERE CreatedBy = %s AND DataName = %s"""


        file = open("config/config.txt", "r")
        contents = file.read()
        dictionary = ast.literal_eval(contents)
        CreatedBy = dictionary["User"]
        DataName = dictionary["DataName"]
        file.close()

        identity = (CreatedBy, DataName)

        data = []

        try:

            cursor.execute(mysql_read_date_description_query, identity)     # executemany gives error
            data.append(cursor.fetchall())

            cursor.execute(mysql_read_data_query, identity)
            data.append(cursor.fetchall())

        except mysql.connector.Error as error:
            print("Error reading from database {}".format(error))

        return data



dbms = Dbms()
