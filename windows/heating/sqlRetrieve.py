import sys
import mysql.connector
import json
import time

timePrevious = time.time() - 60


def data():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ranger01?",
            database="heating"
        )

        mycursor = mydb.cursor()

        mycursor.execute(
            # "SELECT from_unixtime(timestamp, '%d %m %Y %H:%i:%s'),flueGas, boilerTemp, bufferTop, bufferMid,
            # bufferBottom, hotWater FROM test ORDER BY ID DESC LIMIT 1;"
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


while True:
    if time.time() > timePrevious + 60:
        print(time.ctime())
        data()
        timePrevious = time.time()
