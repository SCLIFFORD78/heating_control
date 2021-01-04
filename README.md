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
