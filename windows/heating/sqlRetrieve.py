import sys
import mysql.connector
import json
import time


def data(mydb):
    try:

        mycursor = mydb.cursor()

        mycursor.execute(
            "SELECT * FROM last_25 ;"
        )

        myresult = mycursor.fetchall()
        data = []
        header = ['Time', 'flueGas', 'boilerTemp', 'bufferTop', 'bufferMid', 'bufferBottom', 'hotWater']

        for x in myresult:
            value = [x[0], x[1], x[2], x[3], x[4], x[5], x[6]]
            data.insert(0, value)
        data.insert(0, header)
        print(data)

        with open('buffertop.txt', 'w') as outfile:
            json.dump(data, outfile)

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

