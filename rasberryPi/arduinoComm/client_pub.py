#/usr/bin/python3

import paho.mqtt.client as mqtt
from urllib.parse import urlparse
import sys
from datetime import datetime
import json
import time
from sense_hat import SenseHat
# import presence_detector


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
#url_str = sys.argv[1]
url_str = "mqtt://broker.hivemq.com:1883/Heating/home"
print(url_str)
url = urlparse(url_str)


base_topic = url.path[1:]

# Connect
if (url.username):
    mqttc.username_pw_set(url.username, url.password)

mqttc.connect(url.hostname, url.port)
mqttc.loop_start()

prev_flueGas = 0
prev_boilerTemp = 0
prev_bufferTop = 0
prev_bufferMid = 0
prev_hotWater = 0
prev_bufferBottom = 0

prev_heartBeat = 3
prev_woodFan = 3
prev_woodCircPump = 3
prev_woodHeatCircPump = 3
prev_oilBoiler = 3
prev_hotWaterValve = 3
prev_switchOver = 3
prev_startButton = 3

lastTime = time.time()
noComms = "noComms"
commsEstablished = "commsEstablished"
lostConnection = 1


try:
    import arduinoComm
    commsEstablished_json=json.dumps({"commsEstablished":1, "timestamp":time.time()})
    mqttc.publish(base_topic+"/commsEstablished", commsEstablished_json)
except:
    commsEstablished_json=json.dumps({"commsEstablished":0, "timestamp":time.time()})
    mqttc.publish(base_topic+"/commsEstablished", commsEstablished_json)
    print("Problem with Arduino connection")

   

# Publish a message to temp every 15 seconds
while True:
    try:
        arduinoComm.getValueArduino()

        heartBeat=arduinoComm.states["heartBeat"]
        if heartBeat == prev_heartBeat:
            print("Missed Heart Beat ")
            print(time.time())
            if time.time() > lastTime + 60 and lostConnection == 1:#60 second of no heartbeat
                print("no comms")
                heartBeatLoss_json=json.dumps({"heartBeatLoss":1, "timestamp":time.time()})
                mqttc.publish(base_topic+"/heartBeatLoss", heartBeatLoss_json)
                #lostConnection = 0
                
        if heartBeat != prev_heartBeat:
            #heartBeat_json=json.dumps({"heartBeat":heartBeat, "timestamp":time.time()})
            #mqttc.publish(base_topic+"/heartBeat", heartBeat_json)
            prev_heartBeat = heartBeat
            lastTime = time.time()
            #lostConnection = 0

        
        flueGas=int(arduinoComm.values["flueGas"])
        if flueGas != prev_flueGas:
            flueGas_json=json.dumps({"flueGas":flueGas, "timestamp":time.time()})
            mqttc.publish(base_topic+"/flueGas", flueGas_json)
            prev_flueGas = flueGas
        
        boilerTemp=int(arduinoComm.values["boilerTemp"])
        if boilerTemp != prev_boilerTemp:
            boilerTemp_json=json.dumps({"boilerTemp":boilerTemp, "timestamp":time.time()})
            mqttc.publish(base_topic+"/boilerTemp", boilerTemp_json)
            prev_boilerTemp = boilerTemp
        
        bufferTop=int(arduinoComm.values["bufferTop"])
        if bufferTop != prev_bufferTop:
            bufferTop_json=json.dumps({"bufferTop":bufferTop, "timestamp":time.time()})
            mqttc.publish(base_topic+"/bufferTop", bufferTop_json)
            prev_bufferTop = bufferTop
        
        bufferMid=int(arduinoComm.values["bufferMid"])
        if bufferMid != prev_bufferMid:
            bufferMid_json=json.dumps({"bufferMid":bufferMid, "timestamp":time.time()})
            mqttc.publish(base_topic+"/bufferMid", bufferMid_json)
            prev_bufferMid = bufferMid
        
        hotWater=int(arduinoComm.values["hotWater"])
        if hotWater != prev_hotWater:
            hotWater_json=json.dumps({"hotWater":hotWater, "timestamp":time.time()})
            mqttc.publish(base_topic+"/hotWater", hotWater_json)
            prev_hotWater = hotWater
        
        bufferBottom=int(arduinoComm.values["bufferBottom"])
        if bufferBottom != prev_bufferBottom:
            bufferBottom_json=json.dumps({"bufferBottom":bufferBottom, "timestamp":time.time()})
            mqttc.publish(base_topic+"/bufferBottom", bufferBottom_json)
            prev_bufferBottom = bufferBottom
            
           
            
        woodCircPump=arduinoComm.states["woodCircPump"]
        if woodCircPump != prev_woodCircPump:
            woodCircPump_json=json.dumps({"woodCircPump":woodCircPump, "timestamp":time.time()})
            mqttc.publish(base_topic+"/woodCircPump", woodCircPump_json)
            prev_woodCircPump = woodCircPump
            
        woodHeatCircPump=arduinoComm.states["woodHeatCircPump"]
        if woodHeatCircPump != prev_woodHeatCircPump:
            woodHeatCircPump_json=json.dumps({"woodHeatCircPump":woodHeatCircPump, "timestamp":time.time()})
            mqttc.publish(base_topic+"/woodHeatCircPump", woodHeatCircPump_json)
            prev_woodHeatCircPump = woodHeatCircPump
            
        woodFan=arduinoComm.states["woodFan"]
        if woodFan != prev_woodFan:
            woodFan_json=json.dumps({"woodFan":woodFan, "timestamp":time.time()})
            mqttc.publish(base_topic+"/woodFan", woodFan_json)
            prev_woodFan = woodFan
            
        startButton=arduinoComm.states["startButton"]
        if startButton != prev_startButton:
            startButton_json=json.dumps({"startButton":startButton, "timestamp":time.time()})
            mqttc.publish(base_topic+"/startButton", startButton_json)
            prev_startButton = startButton
            
        oilBoiler=arduinoComm.states["oilBoiler"]
        if oilBoiler != prev_oilBoiler:
            oilBoiler_json=json.dumps({"oilBoiler":oilBoiler, "timestamp":time.time()})
            mqttc.publish(base_topic+"/oilBoiler", oilBoiler_json)
            prev_oilBoiler = oilBoiler
            
        switchOver=arduinoComm.states["switchOver"]
        if switchOver != prev_switchOver:
            switchOver_json=json.dumps({"switchOver":switchOver, "timestamp":time.time()})
            mqttc.publish(base_topic+"/switchOver", switchOver_json)
            prev_switchOver = switchOver
            
        hotWaterValve=arduinoComm.states["hotWaterValve"]
        if hotWaterValve != prev_hotWaterValve:
            hotWaterValve_json=json.dumps({"hotWaterValve":hotWaterValve, "timestamp":time.time()})
            mqttc.publish(base_topic+"/hotWaterValve", hotWaterValve_json)
            prev_hotWaterValve = hotWaterValve
            
    #     temp=round(sense.get_temperature(),2)
    #     temp_json=json.dumps({"temperature":temp, "timestamp":time.time()})
    #     mqttc.publish(base_topic+"/temperature", temp_json)
    #     devices_found_json=json.dumps(presence_detector.find_devices())
    #     if 'name' in devices_found_json:
    #      mqttc.publish(base_topic+"/devices", devices_found_json)
        time.sleep(1)
        arduinoComm.states["heartBeat"]=0
    except:
        print("comms error")
        if lostConnection == 1:
            commsEstablished_json=json.dumps({"commsEstablished":0, "timestamp":time.time()})
            mqttc.publish(base_topic+"/commsEstablished", commsEstablished_json)
            lostConnection = 0
