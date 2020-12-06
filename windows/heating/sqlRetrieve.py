import sys
import mysql.connector
import json
import time


try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ranger01?",
        database="mqtt"
    )
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))


def data():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT bufferaverage AS Temp, from_unixtime(timestamp, '%d %m %Y %H %H:%i:%s') AS Time "
                     "FROM bufferaverage ORDER BY id DESC LIMIT 20")

    myresult = mycursor.fetchall()
    data = []
    header = ['Time', 'Temperature']


    for x in myresult:
        value = [x[1], x[0]]
        data.insert(0, value)
    data.insert(0, header)
    print(data)

    with open('buffertop.txt', 'w') as outfile:
        json.dump(data, outfile)

while True:
    data()
    time.sleep(120)