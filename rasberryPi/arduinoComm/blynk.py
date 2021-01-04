import blynklib
import json

BLYNK_AUTH = 'QfN7Wl86JaC8b-SRH6rPuI4eMH_wIUBv'


outstates={"switchOver":0, "startButton":0}
overwrite={"flueGas":0, "boilerTemp":0}

# initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

#reads current states and values from json files
with open('instates.json','r') as json_file:
    states = json.load(json_file)
    
with open('values.json','r') as json_file:
    values = json.load(json_file)

    
# register handler for virtual pin V0(bufferTop) reading
@blynk.handle_event('read V0')
def read_virtual_pin_handler(pin):
    global values
    temp=values['bufferTop']
    print('Buffer Top: ' + str(temp))  # print temp to console
    blynk.virtual_write(pin, temp)

# register handler for virtual pin V1(boilerTemp) reading  
@blynk.handle_event('read V1')
def read_virtual_pin_handler(pin):
    global values
    with open('values.json','r') as json_file:  #values updated every 2 seconds from blynk app
        values = json.load(json_file)
    temp=values['boilerTemp']
    print('Boiler Temp: ' + str(temp))  # print temp to console
    blynk.virtual_write(pin, temp)

# register handler for virtual pin V2(hotWater) reading
@blynk.handle_event('read V2')
def read_virtual_pin_handler(pin):
    global values
    temp=values['hotWater']
    print('hotwater: ' + str(temp))  # print temp to console
    blynk.virtual_write(pin, temp)
    
# register handler for virtual pin V3(flueGas) reading
@blynk.handle_event('read V3')
def read_virtual_pin_handler(pin):
    global values
    temp= values['flueGas']
    print('Flue Gas: ' + str(temp))  # print temp to console
    blynk.virtual_write(pin, temp)

#register handler for virtual pin V4(startButton) write event
@blynk.handle_event('write V4')
def write_virtual_pin_handler(pin, value):
    outstates['startButton'] = int(value[0])
    print('Start Button:'+ str(value))
    with open('outstates.json','w') as json_file:
        json.dump(outstates,json_file)
    
#register handler for virtual pin V6(switchOver) write event
@blynk.handle_event('write V6')
def write_virtual_pin_handler(pin, value):
    outstates['switchOver'] = int(value[0])
    print('switch Over:'+ str(value))
    with open('outstates.json','w') as json_file:
        json.dump(outstates,json_file)

        
# register handler for virtual pin V(7) writing
@blynk.handle_event('write V7')
def write_virtual_pin_handler(pin, value):
    overwrite['flueGas'] = int(value[0])
    print('Overwrite fluegas:'+ str(value))
    with open('overwrite.json','w') as json_file:
        json.dump(overwrite,json_file)
        print(overwrite)

# register handler for virtual pin V(8) writing
@blynk.handle_event('write V8')
def write_virtual_pin_handler(pin, value):
    overwrite['boilerTemp'] = int(value[0])
    print('Overwrite boilerTemp:'+ str(value))
    with open('overwrite.json','w') as json_file:
        json.dump(overwrite,json_file)
        print(overwrite)


while True:
    blynk.run()
