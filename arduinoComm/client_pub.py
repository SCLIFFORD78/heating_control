#/usr/bin/python3

import paho.mqtt.client as mqtt
from urllib.parse import urlparse
import sys
import time
import json
from sense_hat import SenseHat
# import presence_detector
import arduinoComm

sense = SenseHat()
sense.clear()

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("Connection Result: " + str(rc))

def on_publish(client, obj, mid):
    print("Message ID: " + str(mid))

mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

# parse mqtt url for connection details
url_str = sys.argv[1]
# url_str = "mqtt://broker.hivemq.com:1883/Heating/home"
print(url_str)
url = urlparse(url_str)


base_topic = url.path[1:]

# Connect
if (url.username):
    mqttc.username_pw_set(url.username, url.password)

mqttc.connect(url.hostname, url.port)
mqttc.loop_start()

# Publish a message to temp every 15 seconds
while True:
    arduinoComm.getValueArduino()
    flueGas=arduinoComm.values["flueGas"]
    flueGas_json=json.dumps({"flueGas":flueGas, "timestamp":time.time()})
    mqttc.publish(base_topic+"/flueGas", flueGas_json)
    boierTemp=arduinoComm.values["boierTemp"]
    boierTemp_json=json.dumps({"boierTemp":boierTemp, "timestamp":time.time()})
    mqttc.publish(base_topic+"/boierTemp", boierTemp_json)
    bufferTop=arduinoComm.values["bufferTop"]
    bufferTop_json=json.dumps({"bufferTop":bufferTop, "timestamp":time.time()})
    mqttc.publish(base_topic+"/bufferTop", bufferTop_json)
    bufferMid=arduinoComm.values["bufferMid"]
    bufferMid_json=json.dumps({"bufferMid":bufferMid, "timestamp":time.time()})
    mqttc.publish(base_topic+"/bufferMid", bufferMid_json)
    hotWater=arduinoComm.values["hotWater"]
    hotWater_json=json.dumps({"hotWater":hotWater, "timestamp":time.time()})
    mqttc.publish(base_topic+"/hotWater", hotWater_json)
    bufferBottom=arduinoComm.values["bufferBottom"]
    bufferBottom_json=json.dumps({"bufferBottom":bufferBottom, "timestamp":time.time()})
    mqttc.publish(base_topic+"/bufferBottom", bufferBottom_json)
#     temp=round(sense.get_temperature(),2)
#     temp_json=json.dumps({"temperature":temp, "timestamp":time.time()})
#     mqttc.publish(base_topic+"/temperature", temp_json)
#     devices_found_json=json.dumps(presence_detector.find_devices())
#     if 'name' in devices_found_json:
#      mqttc.publish(base_topic+"/devices", devices_found_json)
    time.sleep(1)
    arduinoComm.states["heartBeat"]=0
