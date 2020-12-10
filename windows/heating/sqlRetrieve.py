import sys
import mysql.connector
import json
import time

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ranger01?",
        database="heating"
    )
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))


def data():
    mycursor = mydb.cursor()

    mycursor.execute(
        "SELECT from_unixtime(timestamp, '%d %m %Y %H:%i:%s'),flueGas, boilerTemp, bufferTop, bufferMid, bufferBottom, hotWater FROM test ORDER BY ID DESC LIMIT 20;")

    myresult = mycursor.fetchall()
    data = []
    header = ['Time', 'flueGas', 'boilerTemp', 'bufferTop', 'bufferMid', 'bufferBottom', 'hotWater']

    for x in myresult:

        value = [x[0], x[1], x[2], x[3], x[4], x[5], x[6] ]
        data.insert(0, value)
    data.insert(0, header)
    print(data)

    with open('buffertop.txt', 'w') as outfile:
        json.dump(data, outfile)


while True:
    data()
    time.sleep(60)
