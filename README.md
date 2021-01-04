# heating_control
SMART HEATING CONTROL AND ANALYTICS OF INTEGRATED OIL AND SOLID FUEL HEATING SYSTEM

Student Name:	Sheamus Clifford	Student ID:	02794331

Description:
For my computer systems and networks assignment I intend to implement a smart heating control system which will also record relevant data to a MySQL database for further analysis in order to optimise heating control.
The heating system itself will consist of a traditional oil-fired boiler and a wood fired gasification boiler. My intention is measure and control the relevant influencing factors and to control the heating function and switching between oil and gasification systems. A description of how wood gasification works can be found at the following link. http://www.greenheat.ie/products/boilers/wood-gasification-boilers/
Aside from being able to control the system over a network my primary focus is the real time data I wish to obtain from the system while in operation. I want to employ industry 4.0 principles for my project, in particular:
1. Data being edge driven
2. Report by exception
3. Data interpreted and analysed in a meaningful way and results fed back into the system to form a closed loop in order to optimise and control it based on complete system influencing factors.

Tools, Technologies, and Equipment:
During the implementation of my project I propose to use the following:
1. Arduino Uno control boards x 2
2. Raspberry Pi with Sense Hat
3. LCD display panel
4. Thermocouple temperature sensors x 2
5. 4 x PT100 temperature sensors using I2C communication
6. Push buttons for control
7. MQTT Publish and Subscribe
8. http protocol for commands
9. MySQL to store data
10. Python and C++ coding for Raspberry Pi and Arduinos


See Presentation.pptx for an overview of the system setup and overview of system operation

1. The heating control system has been created on an Arduino Uno. This controller receives sensor values and actuates process pumps valves and fans through relays.
2. A raspberry Pi controls communication, receives sensor values and states from control Arduino and sends data via MQTT to a local server to store data. Raspberry Pi also syncs   data with Blynk app for easy monitoring and switching of process controls remotely. Raspberry Pi also sends external control signals back down to control Arduino via serial connection based on remote inputs from Blynk app.
3. Remote server receives data from Raspberry Pi at remote location and stores data to MySql server for future analysis. Server also sends data to thingspeak for remote storage and monitoring if required.
4. Thingspeak has a React set up to send a tweet if data has not been received for more than 60 mins, this will alert user that the system is offline and not sending data. Also a react is sent if the temperature of the buffer tank drops below 60 degrees, so user can light gasification boiler in time to get up to heat to prevent system switching over to oil fired heating.
4. Blynk app displays critical values to user, has a notification set to alert user if temperature of the buffer tank drops below a threshold in order for user to light fire for gasification boiler. Also a notification to notify user if hardware goes offline to signal communication issues with Raspberry Pi or other problems which may cause communication loss i.e. power loss, network loss or hardware failure.


ADDED THE FOLLOWING TO RASPBERRY PI IN ORDER TO RUN ON BOOT:

added blynk.py to run on boot in rc.local by adding th following code : sudo nano /etc/rc.local
    cd /home/pi/Assignment2/arduinoComm
    sudo python3 blynk.py &

added client_pub.py to run on boot .bashrc by adding the following code to : sudo nano /home/pi/.bashrc
    cd /home/pi/Assignment2/arduinoComm
    python3 blynk.py
note: for bashrc this runs code in shell window, just open shell shortcut and client_pub.py will be running. need to to add 'chmod+x client_pub.py' before this will work!!

THINGSPEAK:
    Currently i have a thingspeak channel with features as described above channel ID: 1242209

you tube combined overview video http://www.youtube.com/watch?v=F-mWeRQDeKE
individual explaination videos also added

sql dump file located in SQL folder