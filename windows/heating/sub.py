#!/usr/bin/python3

import paho.mqtt.client as mqtt
from urllib.parse import urlparse
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


# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("Connection Result: " + str(rc))

def on_message(client, obj, msg):
    # Prepare Data, separate columns and values
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("message received",m_decode)
    m_in=json.loads(m_decode)
    #columns = ', '.join(m_in.keys())+""
    column1 = list(m_in.keys())[0]
    column2 = list(m_in.keys())[1]
    value1 = list(m_in.values())[0]
    value2 = list(m_in.values())[1]
    if column1 != "heartBeat":
        mycursor = mydb.cursor()
        createTable = "CREATE TABLE IF NOT EXISTS %s(ID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,%s INT,%s VARCHAR(255))"%(column1,column1,column2)
        sql = "INSERT INTO %s (%s,%s) VALUES (%s,%s)" %(column1,column1,column2,value1,value2)
        mycursor.execute(createTable)
        mycursor.execute(sql)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed,  QOS granted: "+ str(granted_qos))

mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# parse mqtt url for connection details
#url_str = sys.argv[1]
url_str = "mqtt://broker.hivemq.com:1883/Heating/home"
url = urlparse(url_str)
base_topic = url.path[1:]

# Connect
if (url.username):
    mqttc.username_pw_set(url.username, url.password)
print(url.hostname)
print(url.port)
mqttc.connect(url.hostname, url.port)

# Start subscribe, with QoS level 2
mqttc.subscribe(base_topic+"/#", 2)
mqttc.loop_forever()

# Continue the network loop, exit when an error occurs
heartBeat = 0
rc = 0
while rc == 0:

    rc = mqttc.loop()

print("rc: " + str(rc))
