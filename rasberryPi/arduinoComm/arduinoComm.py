#!/usr/bin/env python
import time
import serial
import json

#port 1 is for comms to arduino controlling the thermocouple values of boiler temp and flueas temp (Nano)
port1 = serial.Serial(
        port='/dev/ttyUSB1', 
        baudrate = 57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

#port 2 is the main control arduino (Uno)
port2 = serial.Serial(
        port='/dev/ttyUSB0', 
        baudrate = 57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

flueGas=boilerTemp=bufferTop=bufferMid=hotWater=bufferBottom =0.00
values={"flueGas":flueGas,"boilerTemp":boilerTemp,"bufferTop":bufferTop,"bufferMid":bufferMid ,"hotWater":hotWater,"bufferBottom":bufferBottom}

heartBeat=woodFan= woodCircPump= woodHeatCircPump= oilBoiler= hotWaterValve= switchOver= startButton=0
states={"heartBeat":heartBeat,"woodFan":woodFan, "woodCircPump":woodCircPump, "woodHeatCircPump":woodHeatCircPump, "oilBoiler":oilBoiler, "hotWaterValve":hotWaterValve, "switchOver":switchOver, "startButton":startButton}

#takes the states of relays for control and the values of measured tempearture values and created an array of each
def feedBack(serial_data,values,states):    
    if len(serial_data)>13:
        for i in range(6):
            serial_data[i]=float(serial_data[i])
        for i in range(6,len(serial_data)):
            serial_data[i]=int(serial_data[i])
        values["flueGas"]= serial_data[0]
        values["boilerTemp"]= serial_data[1]
        values["bufferTop"]= serial_data[2]
        values["bufferMid"]= serial_data[3]
        values["hotWater"]= serial_data[4]
        values["bufferBottom"]= serial_data[5]
        states["heartBeat"]= 1
        states["woodFan"]= serial_data[7]
        states["woodCircPump"]= serial_data[8]
        states["woodHeatCircPump"]= serial_data[9]
        states["oilBoiler"]= serial_data[10]
        states["hotWaterValve"]= serial_data[11]
        states["switchOver"]= serial_data[12]
        states["startButton"]= serial_data[13]
        return values
        return states
        

# gets values from arduino serial comms and then seperates into arrays of values and states by passing to feedback function       
def getValueArduino():
    while 1:
            with open('overwrite.json','r') as json_file:   #simulated values from blynk app
                    overwrite = json.load(json_file)
                    overwrite_fluegas = overwrite['flueGas'] + 100
                    overwrite_boilerTemp = overwrite['boilerTemp'] + 100
                    temp = str(overwrite_boilerTemp)+str(overwrite_fluegas)

# The following code is not used as thermoucouplier readings proving unreliable, will swap out with PT1000 sensors but wont have in time for project deadline
#   will simulate values from blynk app for now for temperatures for fluegas and boiler
#
#            if port1.isOpen():
#                port1.write("Write counter: Test1 \n".encode())
#                time.sleep(1)
#                temp=""
#                try:
#                    #reading thermocouplier values
#                    temp=str(port1.readline(),'ascii')
#                    #print("values from thermo to be sent to main arduino ",temp)
#                except UnicodeDecodeError:
#                    print("")
#                time.sleep(1)
#            else:
#                print("error1")
            if port2.isOpen():
                with open('outstates.json','r') as json_file:
                    outstates = json.load(json_file)
                
                temp = temp[ : 6] + str(outstates['switchOver'])+str(outstates['startButton'])#adds switching ststes from blynk app for switching on main control Arduino(Uno)
                port2.write(temp.encode())#write thermocouplier values to to main arduino
                time.sleep(1)
                temp2=port2.readline()#read data from main arduino
                temp3=[]
                try:
                    temp2=str(temp2,'ascii')
                    temp3=temp2.rstrip().split(",")
                except UnicodeDecodeError:
                    print("UnicodeDecodeError reading data from main Arduino")
                time.sleep(1)
                if len(temp3)>13:
                    feedBack(temp3,values,states)
            else:
                print("error2")
            return values,states
            time.sleep(1)
            
while states["heartBeat"]==0:   #arduino sends a heartbea value of '0' once recieved this value is set to 1 by feedback function and returned to main program client_sub.py
    getValueArduino()           #this ensures that arduinoComm only runs once, heatbeat monitoring done in main client_sub.py

