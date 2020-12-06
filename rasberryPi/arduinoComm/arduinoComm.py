#!/usr/bin/env python
import time
import serial
import json

port1 = serial.Serial(
        port='/dev/ttyUSB0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

port2 = serial.Serial(
        port='/dev/ttyUSB1', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
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
#         for i in range(6):
#             values[i]=float(serial_data[i])
#         for i in range(6,len(serial_data)):
#             states[i-6]=int(serial_data[i])
        return values
        return states
def getValueArduino():
    while 1:
            if port1.isOpen():
    #           port1.write("Write counter: Test1 \n".encode())
                time.sleep(1)
                temp=""
                try:
                    #reading thermocouplier values
                    temp=str(port1.readline(),'ascii')
                    print("values from thermo to be sent to main arduino ",temp)
                except UnicodeDecodeError:
                    print("")
                time.sleep(1)
            else:
                print("error1")
            if port2.isOpen():
                with open('outstates.json','r') as json_file:
                    outstates = json.load(json_file)
                    print(outstates)
                
                temp = temp[ : 6] + str(outstates['switchOver'])+str(outstates['startButton'])
                print("values from thermo to be sent to main arduino with outstates",temp)
                port2.write(temp.encode())#write thermocouplier values to to main arduino
                time.sleep(1)
                temp2=port2.readline()
                temp3=[]
                try:
                    temp2=str(temp2,'ascii')
                    temp3=temp2.rstrip().split(",")
    #                 print(temp3)
                except UnicodeDecodeError:
                    print("")
                time.sleep(1)
                if len(temp3)>13:
                    feedBack(temp3,values,states)
            else:
                print("error2")
            return values,states
            time.sleep(1)
            
while states["heartBeat"]==0:
    getValueArduino()

