#/usr/bin/python3

import paho.mqtt.client as mqtt
from urllib.parse import urlparse
import sys
from datetime import datetime
import json
import time
from sense_hat import SenseHat


sense = SenseHat()
sense.clear()
blue = (0, 0, 255)
red = (255,0,0)

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

mqttc.connect(url.hostname, url.port,43200)
mqttc.loop_start()

prev_flueGas = 0
prev_boilerTemp = 0
prev_bufferTop = 0
prev_bufferMid = 0
prev_hotWater = 0
prev_bufferBottom = 0
prev_bufferAverage = 0

prev_heartBeat = 3
prev_woodFan = 3
prev_woodCircPump = 3
prev_woodHeatCircPump = 3
prev_oilBoiler = 3
prev_hotWaterValve = 3
prev_switchOver = 3
prev_startButton = 3

states={"woodFan" :-1, "woodCircPump" :-1, "woodHeatCircPump" :-1, "oilBoiler" :-1, "hotWaterValve" :-1, "switchOver" :-1, "startButton" :-1}
values={"flueGas" :0,"boilerTemp" :0,"bufferTop" :0,"bufferMid" :0,"hotWater" :0,"bufferBottom" :0}


lastTime = time.time()
noComms = "noComms"
commsEstablished = "commsEstablished"
lostConnection = 1
average = []

#if arduinoComm imports succsefully then comms established by all devices if not of if a device not online the error message is given
try:
    import arduinoComm
    commsEstablished_json=json.dumps({"commsEstablished":1, "timestamp":time.time()})
    mqttc.publish(base_topic+"/commsEstablished", commsEstablished_json,2)
except:
    commsEstablished_json=json.dumps({"commsEstablished":0, "timestamp":time.time()})
    mqttc.publish(base_topic+"/commsEstablished", commsEstablished_json,2)
    print("Problem with Arduino connection")

   

# Publish 
while True:
    try:
        arduinoComm.getValueArduino()   # getts states and values from Arduino    

        #if arduinos and Pi have not communicated successfully for more than 60 seconds and heartbeat value hasnt changed then flag is raised
        heartBeat=arduinoComm.states["heartBeat"]
        if heartBeat == prev_heartBeat:
            print("Missed Heart Beat ")
            print(time.time())
            if time.time() > lastTime + 60 and lostConnection == 1:#60 second of no heartbeat
                print("no comms")
                heartBeatLoss_json=json.dumps({"heartBeatLoss":1, "timestamp":time.time()})
                mqttc.publish(base_topic+"/heartBeatLoss", heartBeatLoss_json,2)
                lastTime = time.time()
                
        if heartBeat != prev_heartBeat:
            prev_heartBeat = heartBeat
            lastTime = time.time()

        
        flueGas=int(arduinoComm.values["flueGas"])
        if flueGas >=120:
            sense.show_message("Fine!", text_colour = red)
        else:
            sense.show_message("COLD!", text_colour = blue)
        
        with open('outstates.json','r') as json_file:
            outstates = json.load(json_file)
        if flueGas != prev_flueGas:
            if flueGas > 0:
                flueGas_json=json.dumps({"flueGas":flueGas, "timestamp":time.time()})
                mqttc.publish(base_topic+"/flueGas", flueGas_json,2)
            values['flueGas']=flueGas
            prev_flueGas = flueGas
        

        boilerTemp=int(arduinoComm.values["boilerTemp"])
        #temp of thermocouple fluctuated alot, this code averages the value over 10 readings
        if len(average) < 11:
            average.append(boilerTemp)
        else:
            average.pop(0)
            average.append(boilerTemp)
        avg = 0
        for i in average:
            avg = avg + i
        avg = avg / len(average)
        boilerTemp = round(avg)
        #to further reduce fluctuation a change of 5 degrees is needed 
        if (boilerTemp > prev_boilerTemp+5) or (boilerTemp < prev_boilerTemp-5):
            if boilerTemp >0:
                boilerTemp_json=json.dumps({"boilerTemp":boilerTemp, "timestamp":time.time()})
                mqttc.publish(base_topic+"/boilerTemp", boilerTemp_json,2)
            values['boilerTemp']=boilerTemp
            prev_boilerTemp = boilerTemp
        
        bufferTop=int(arduinoComm.values["bufferTop"])
        if bufferTop != prev_bufferTop:
            if bufferTop >0:
                bufferTop_json=json.dumps({"bufferTop":bufferTop, "timestamp":time.time()})
                mqttc.publish(base_topic+"/bufferTop", bufferTop_json,2)
            values['bufferTop']=bufferTop
            prev_bufferTop = bufferTop
        
        bufferMid=int(arduinoComm.values["bufferMid"])
        if bufferMid != prev_bufferMid:
            if bufferMid >0:
                bufferMid_json=json.dumps({"bufferMid":bufferMid, "timestamp":time.time()})
                mqttc.publish(base_topic+"/bufferMid", bufferMid_json,2)
            values['bufferMid']=bufferMid
            prev_bufferMid = bufferMid
        
        hotWater=int(arduinoComm.values["hotWater"])
        if hotWater != prev_hotWater:
            if hotWater >0:
                hotWater_json=json.dumps({"hotWater":hotWater, "timestamp":time.time()})
                mqttc.publish(base_topic+"/hotWater", hotWater_json,2)
            values['hotWater']=hotWater
            prev_hotWater = hotWater
        
        bufferBottom=int(arduinoComm.values["bufferBottom"])
        if bufferBottom != prev_bufferBottom:
            if bufferBottom >0:
                bufferBottom_json=json.dumps({"bufferBottom":bufferBottom, "timestamp":time.time()})
                mqttc.publish(base_topic+"/bufferBottom", bufferBottom_json,2)
            values['bufferBottom']=bufferBottom
            prev_bufferBottom = bufferBottom

        bufferAverage=int((bufferTop + bufferMid + bufferBottom)/3)
        if bufferAverage != prev_bufferAverage:
            bufferAverage_json=json.dumps({"bufferAverage":bufferAverage, "timestamp":time.time()})
            mqttc.publish(base_topic+"/bufferAverage", bufferAverage_json,2)
            prev_bufferAverage = bufferAverage
            
           
            
        woodCircPump=arduinoComm.states["woodCircPump"]
        if woodCircPump != prev_woodCircPump:
            woodCircPump_json=json.dumps({"woodCircPump":woodCircPump, "timestamp":time.time()})
            mqttc.publish(base_topic+"/woodCircPump", woodCircPump_json,2)
            states['woodCircPump'] = woodCircPump
            prev_woodCircPump = woodCircPump
            
        woodHeatCircPump=arduinoComm.states["woodHeatCircPump"]
        if woodHeatCircPump != prev_woodHeatCircPump:
            woodHeatCircPump_json=json.dumps({"woodHeatCircPump":woodHeatCircPump, "timestamp":time.time()})
            mqttc.publish(base_topic+"/woodHeatCircPump", woodHeatCircPump_json,2)
            states['woodHeatCircPump'] = woodHeatCircPump
            prev_woodHeatCircPump = woodHeatCircPump
            
        woodFan=arduinoComm.states["woodFan"]
        if woodFan != prev_woodFan:
            woodFan_json=json.dumps({"woodFan":woodFan, "timestamp":time.time()})
            mqttc.publish(base_topic+"/woodFan", woodFan_json,2)
            states['woodFan'] = woodFan
            prev_woodFan = woodFan
            
        startButton=arduinoComm.states["startButton"]
        if startButton != prev_startButton:
            startButton_json=json.dumps({"startButton":startButton, "timestamp":time.time()})
            mqttc.publish(base_topic+"/startButton", startButton_json,2)
            states['startButton'] = startButton
            prev_startButton = startButton
            
        oilBoiler=arduinoComm.states["oilBoiler"]
        if oilBoiler != prev_oilBoiler:
            oilBoiler_json=json.dumps({"oilBoiler":oilBoiler, "timestamp":time.time()})
            mqttc.publish(base_topic+"/oilBoiler", oilBoiler_json,2)
            states['oilBoiler'] = oilBoiler
            prev_oilBoiler = oilBoiler
            
        switchOver=arduinoComm.states["switchOver"]
        if switchOver != prev_switchOver:
            switchOver_json=json.dumps({"switchOver":switchOver, "timestamp":time.time()})
            mqttc.publish(base_topic+"/switchOver", switchOver_json,2)
            states['switchOver'] = switchOver
            prev_switchOver = switchOver
            
        hotWaterValve=arduinoComm.states["hotWaterValve"]
        if hotWaterValve != prev_hotWaterValve:
            hotWaterValve_json=json.dumps({"hotWaterValve":hotWaterValve, "timestamp":time.time()})
            mqttc.publish(base_topic+"/hotWaterValve", hotWaterValve_json,2)
            prev_hotWaterValve = hotWaterValve
            

        with open ('instates.json', 'w') as instate:#in states from Arduino
            json.dump(states,instate)
        with open ('values.json', 'w') as invalues:#read values from arduino
            json.dump(values,invalues)
        time.sleep(1)
        arduinoComm.states["heartBeat"]=0 

        
    except:
        print("comms error")
        if lostConnection == 1:
            commsEstablished_json=json.dumps({"commsEstablished":0, "timestamp":time.time()})
            mqttc.publish(base_topic+"/commsEstablished", commsEstablished_json,2)
            lostConnection = 0
