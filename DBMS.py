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
                                                      database = database)
            self.cursor = self.connection.cursor

        except mysql.connector.Error as error:
            print("Failed to connect {}".format(error))

        finally:
            if self.connection.is_connected():
                print("Connection Established")



    def save_to_database(self, data):
        cursor = self.connection.cursor()

        mySql_insert_query = """INSERT INTO ypr (Time, Yaw, Pitch, Roll)
                                          VALUES (%s, %s, %s, %s) """
        cursor.executemany(mySql_insert_query, data)
        self.connection.commit()

        print("successfully saved to database")

    def read_from_database(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT Time, Yaw, Pitch, Roll FROM ypr")
        data = cursor.fetchall()
        print(data)
        return data



dbms = Dbms()