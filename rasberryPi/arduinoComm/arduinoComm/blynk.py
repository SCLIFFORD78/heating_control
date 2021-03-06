import blynklib
from sense_hat import SenseHat
import json

BLYNK_AUTH = 'QfN7Wl86JaC8b-SRH6rPuI4eMH_wIUBv'


sense = SenseHat()

#clear sensehat and intialise light_state
sense.clear()

outstates={"switchOver":0, "startButton":0}
overwrite={"flueGas":0, "boilerTemp":0}

# initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)
with open('instates.json','r') as json_file:
    states = json.load(json_file)
    print(states)
    
with open('values.json','r') as json_file:
    values = json.load(json_file)

# register handler for virtual pin V1 write event
#@blynk.handle_event('write V1')
#def write_virtual_pin_handler(pin, value):
    #print('V1:'+ str(value))
    #r=int(value[0]) # or you could do this: value = list(map(int, value))
    #g=int(value[1])
    #b=int(value[2])
    #sense.clear(r,g,b)
    
# register handler for virtual pin V2(temperature) reading
@blynk.handle_event('read V0')
def read_virtual_pin_handler(pin):
    global values
    #with open('values.json','r') as json_file:
    #    values = json.load(json_file)
    temp=values['bufferTop']
    print('Buffer Top: ' + str(temp))  # print temp to console
    blynk.virtual_write(pin, temp)
    
@blynk.handle_event('read V1')
def read_virtual_pin_handler(pin):
    global values
    with open('values.json','r') as json_file:
        values = json.load(json_file)
    temp=values['boilerTemp']
    print('Boiler Temp: ' + str(temp))  # print temp to console
    blynk.virtual_write(pin, temp)

# register handler for virtual pin V2(temperature) reading
@blynk.handle_event('read V2')
def read_virtual_pin_handler(pin):
    global values
    #with open('values.json','r') as json_file:
    #    values = json.load(json_file)
    temp=values['hotWater']
    print('hotwater: ' + str(temp))  # print temp to console
    blynk.virtual_write(pin, temp)
    
# register handler for virtual pin V2(temperature) reading
@blynk.handle_event('read V3')
def read_virtual_pin_handler(pin):
    global values
    #with open('values.json','r') as json_file:
    #    values = json.load(json_file)
    temp= values['flueGas']
    print('Flue Gas: ' + str(temp))  # print temp to console
    blynk.virtual_write(pin, temp)

#register handler for virtual pin V4(light sensor) write event
@blynk.handle_event('write V4')
def write_virtual_pin_handler(pin, value):
    outstates['startButton'] = int(value[0])
    print('Start Button:'+ str(value))
    with open('outstates.json','w') as json_file:
        json.dump(outstates,json_file)
        print(outstates)

# register handler for virtual pin V(woodFan) reading
@blynk.handle_event('read V5')
def read_virtual_pin_handler(pin):
    with open('instates.json','r')as json_file:
        instates = json.load(json_file)
    woodFan=instates['woodFan']
    print('Boiler Fan: ' + str(woodFan))  # print state to console
    blynk.virtual_write(pin, woodFan)
    
    
#register handler for virtual pin V4(light sensor) write event
@blynk.handle_event('write V6')
def write_virtual_pin_handler(pin, value):
    outstates['switchOver'] = int(value[0])
    print('switch Over:'+ str(value))
    with open('outstates.json','w') as json_file:
        json.dump(outstates,json_file)
        print(outstates)
        
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
