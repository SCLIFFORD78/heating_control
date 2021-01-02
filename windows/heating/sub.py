#!/usr/bin/python3

import paho.mqtt.client as mqtt
from urllib.parse import urlparse
import sys
import mysql.connector
import json
import time
from urllib.request import urlopen
import numpy
import sqlRetrieve

WRITE_API_KEY = 'COKOEUF7NMOXWNPE'

baseURL = 'https://api.thingspeak.com/update?api_key=%s' % WRITE_API_KEY

fieldValues = {'flueGas': 'field1',
               'boilerTemp': 'field2',
               'bufferTop': 'field3',
               'bufferMid': 'field4',
               'bufferBottom': 'field5',
               'hotWater': 'field6'
               }
storedData = []
delayThingSpeakTime = time.time()
timeNow = time.time()

# parse mqtt url for connection details
# url_str = sys.argv[1]
url_str = "mqtt://broker.hivemq.com:1883/Heating/home"
url = urlparse(url_str)
base_topic = url.path[1:]


def writeData(value, field):
    # sending data to thigspeak in the query string
    conn = urlopen(baseURL + '&%s=%s' % (field, value))
    print(conn.read(), "Field: ", field, " Value: ", value)
    # closing the connection
    conn.close()


def sqlSave(valueName, valueReading, time_stamp):
    try:
        with open('userdata1.json', 'r') as outfile:
            data = json.load(outfile)
            data['timestamp'] = time_stamp
            for x in data:
                if x == valueName and data[x] != valueReading and x != 'timestamp':
                    data[x] = valueReading
                    mycursor = mydb.cursor()
                    sql = "INSERT INTO test (flueGas,boilerTemp,bufferTop,bufferMid,bufferBottom,hotWater,woodFan,woodCircPump,woodHeatCircPump,oilBoiler,hotWaterValve,switchOver,startButton,commsEstablished,`timeStamp`)" \
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (
                              data['flueGas'], data['boilerTemp'], data['bufferTop'], data['bufferMid'],
                              data['bufferBottom'], data['hotWater'], data['woodFan'],
                              data['woodCircPump'], data['woodHeatCircPump'], data['oilBoiler'], data['hotWaterValve'],
                              data['switchOver'], data['startButton'],
                              data['commsEstablished'], data['timestamp'])
                    mycursor.execute(sql)
                    mydb.commit()
                    print(mycursor.rowcount, "record inserted.", time.ctime())
        with open('userdata1.json', 'w') as outfile:
            json.dump(data, outfile)

        sqlRetrieve.data(mydb)
    except:
        print("File Error on opening", time.ctime())


try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ranger01?",
        database="heating"
    )
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))


# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("Connection Result: " + str(rc))
    global timeNow
    if timeNow + 120 < time.time():
        mqttc.reconnect()
        mqttc.subscribe(base_topic + "/#", 2)
        print("Attemt re connect and sub ", time.ctime())
        timeNow = time.time()


def on_message(client, obj, msg):
    global delayThingSpeakTime
    # Prepare Data, separate columns and values
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    print("message received", m_decode)
    m_in = json.loads(m_decode)
    # columns = ', '.join(m_in.keys())+""
    column1 = list(m_in.keys())[0]  # value name e.g. bufferTop
    column2 = list(m_in.keys())[1]  # timestamp
    value1 = list(m_in.values())[0]  # value name: reading
    value2 = list(m_in.values())[1]  # actual timestamp
    sqlSave(column1, value1, value2)
    for i in fieldValues:
        if column1 == i:  # checks if subscribed value is in the array of possible values
            if len(storedData) > 0:
                for j in range(len(storedData)):
                    if fieldValues[i] == storedData[j][1]:  # checks if there is a value in the buffer already
                        storedData[j][0] = value1  # replaces the value in buffer with most recent
                        break
                    if j == len(storedData) - 1 and column1 != storedData[j][1]:
                        store = [value1, fieldValues[i]]
                        storedData.append(store)
                        break
            else:
                store = [value1, fieldValues[i]]
                storedData.append(store)
                break
    if len(storedData) > 0:
        print("DataStorage buffer =  ", len(storedData))
        if time.time() > delayThingSpeakTime + 32:
            writeData(storedData[0][0], storedData[0][1])
            storedData.pop(0)
            delayThingSpeakTime = time.time()
    print(storedData)


def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed,  QOS granted: " + str(granted_qos))


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection." + str(client) + "  ", time.ctime())


mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect

mqttc.enable_logger()

# Connect
if (url.username):
    mqttc.username_pw_set(url.username, url.password)
print(url.hostname)
print(url.port)
mqttc.connect(url.hostname, url.port, 30)

# Start subscribe, with QoS level 2
mqttc.subscribe(base_topic + "/#", 2)
mqttc.loop_forever()

# Continue the network loop, exit when an error occurs
heartBeat = 0
rc = 0

while rc == 0:
    rc = mqttc.loop()

print("rc: " + str(rc) + "No Data is being logged")
