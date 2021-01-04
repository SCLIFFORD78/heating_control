#include <OneWire.h>
#include <DallasTemperature.h>
#include "max6675.h"
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SoftwareSerial.h>

// Set the LCD address to 0x3F for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x3F, 16, 2);
// Data wire is plugged into port A0 on the Arduino
#define ONE_WIRE_BUS 14
OneWire oneWire(ONE_WIRE_BUS);
// Pass our oneWire reference to Dallas Temperature.
DallasTemperature sensors(&oneWire);
int lcdLighOn = 3;
const int startButton = 6;            //Wood boiler start button/row 12/resistor to ground
const int switchOver = 7;             //switch over for supply to boiler from heating - OFF for oil/relay 1/core1/row 14/BBG
const int woodFan = 8;                //gasification boiler fan/relay 2 / core 6 / row16
const int woodCircPump = 13;           //gasification boiler circulating pump internal / relay 3 / core 4 / row 18
const int woodHeatCircPump = 10;      //buffer tank heating pump to house / relay 4 / core 2 / row 20
const int oilBoiler = 11;             //oil boiler and circulating pump .ON for oil, OFF for wood / relay 5 / core earth / row 22
const int hotWaterValve = 12;           //actuator valve for hot water tank / relay 6 / core 5 / row 24
int thermoDO = 17;                    //row 20 (a side)
int thermoCS = 19;                    //row 22 (a side)
int thermoCLK = 18;                   //row 24 (a side)
int BthermoDO = 0;                   //row 18 (a side)
int BthermoCS = 1;                   //row 22 (a side)
int BthermoCLK = 2;                  //row 24 (a side)
MAX6675 thermocouple(thermoCLK, thermoCS, thermoDO);
MAX6675 Bthermocouple(BthermoCLK, BthermoCS, BthermoDO);
long i = 0;
boolean boilerON = false;
bool startDelay = false;
bool lcdBackLightOn = false;
int currentCount = 0;
int count = 0;
int heartBeat = 0;
bool toggle = false;
bool lightSet = false;
int j = 0;
int m = 0;
int y = 0;
String boilerTempint;
long flueGas;
long boilerTemp;
long gasTempCircValue = 78;
float bufferTop;
float bufferMid;
float hotWater;
float bufferBottom;
bool initialiaseGas;
bool initialiaseBoiler;
String valueX = "";
String value7 = "";
String value8 = "";





//Start up sequence for wood boiler

void setup(void) {
  Serial.begin(57600);//USB1
  // Start up the library
  sensors.begin();
  // initialize  outputs:
  pinMode(woodFan, OUTPUT);
  pinMode(woodCircPump, OUTPUT);
  pinMode(woodHeatCircPump, OUTPUT);
  pinMode(oilBoiler, OUTPUT);
  pinMode(hotWaterValve, OUTPUT);
  pinMode(switchOver, OUTPUT);
  pinMode(startButton, INPUT);
  pinMode (lcdLighOn, INPUT);
  pinMode (4, OUTPUT);

  boilerON = false;
  digitalWrite(woodFan, HIGH);
  digitalWrite(woodCircPump, HIGH);
  digitalWrite(woodHeatCircPump, HIGH);
  digitalWrite(oilBoiler, HIGH);
  digitalWrite(hotWaterValve, HIGH);

  initialiaseGas = false;
  initialiaseBoiler = false;


  // initialize the LCD
  lcd.begin();
  lcd.noBacklight();
  delay(50);
}

void loop(void) {
  float bufferTop1 = sensors.getTempCByIndex(0);              //buffer tank top temp+++++++++++++++++4.7k ohm resistor between 5v out and signal back++++++++++++++++++++
  if (bufferTop1 > 10 && bufferTop1 < 100) bufferTop = bufferTop1;
  float bufferMid1 = sensors.getTempCByIndex(1);              //buffer tank middle temp
  if (bufferMid1 > 10 && bufferMid1 < 100) bufferMid = bufferMid1;
  float hotWater1 = sensors.getTempCByIndex(2);              //hot water tank mid temperature
  if (hotWater1 > 10 && hotWater1 < 100) hotWater = hotWater1;
  float bufferBottom1 = sensors.getTempCByIndex(3);          //buffer tank bottom temp
  if (bufferBottom1 > 10 && bufferBottom1 < 100) bufferBottom = bufferBottom1;

  if (Serial.available() > 0)
    valueX = Serial.readString();
  value7 = "";
  value8 = "";
  for (i = 0; i < 3; i++) value7 = value7 + valueX[i];
  for (i = 3; i < valueX.length(); i++)value8 = value8 + valueX[i];

  long value9 = value7.toInt();
  long boilerTemp1 = value9 - 100;
  if (initialiaseBoiler == false) {
    boilerTemp = boilerTemp1;
    initialiaseBoiler = true;
  }
  if (value9 > 0 && value9 < 250 && boilerTemp1 > 5 && boilerTemp1 < 250 ) {
    boilerTemp = boilerTemp1;
  } else {
    boilerTemp = boilerTemp;
  };

  long value10 = value8.toInt();
  long flueGas1 = value10 - 100;
  if (initialiaseGas == false) {
    flueGas = flueGas1;
    initialiaseGas = true;
  }
  if (value10 > 0 && value10 < 250 && flueGas1 > 5 && flueGas1 < 250) {
    flueGas = flueGas1;
  } else {
    flueGas = flueGas;
  };

  //flueGas = map(flueGas,1032,0,0,255);

  // request to all devices on the bus
  sensors.requestTemperatures(); // Send the command to get temperatures
  //*****************************************************************LCD BACKLIGHT CONTROL***************************************************************************************
  lcdBackLightOn = digitalRead(lcdLighOn);
  if (lcdBackLightOn == true) {
    j = 0;
    lcd.backlight();
    m++;
  }
  if (j > 50 && m < 2) {
    lcd.noBacklight();
    m = 0;
  }
  if (lcdBackLightOn == true && m >= 2) {
    toggle = true;
    m = 1;
  }
  if (toggle == true && lcdBackLightOn == LOW) {
    count = count + 1;
    toggle = false;
    lightSet = true;
    lcd.backlight();
    j = 0;
  }
  if (count > 6) {
    count = 0;
  }
  if (lightSet == true && j > 50) {
    lcd.noBacklight();
    lightSet = false;
    j = 0;
  }
  // ***************************************************************switch over for supply to boiler from heating - ON for oil***********************************************
  if (bufferTop < 40) {
    digitalWrite(switchOver, LOW);
  }
  else if (bufferTop > 55 && digitalRead(switchOver) == LOW) {
    digitalWrite(switchOver, HIGH);
  }

  //*************************************************************************boiler on programe*******************************************************************************
  if (i > 3600)startDelay = true;
  if (i <= 3600) startDelay = false;



  if (digitalRead(startButton) == HIGH) {
    boilerON = true;
  }
  if (digitalRead(startButton) == LOW) {
    boilerON = false;
    if (digitalRead(woodFan) == LOW) digitalWrite(woodFan, HIGH);
    i = 0;
  }

  if ( boilerON == true) {
    i++;

    if ((startDelay == false || flueGas > 100) && boilerTemp < 90 && flueGas < 200) { //sub in boiler temp,i=1800(for 60 mins)
      digitalWrite(woodFan, LOW);
    }
    else if ((startDelay == true && flueGas < 100 && digitalRead(woodFan) == LOW)) {
      digitalWrite(woodFan, HIGH);
    }
    else {
      digitalWrite(woodFan, HIGH);
    }
  }
  // *********************************************************************gasification boiler circulating pump internal*******************************************************
  if (boilerTemp >  72) {
    digitalWrite(woodCircPump, LOW);
  }
  if (boilerTemp < 70) {
    digitalWrite(woodCircPump, HIGH);
  }
  //**********************************************************************actuator valve for hot water tank********************************************************************
  if (digitalRead(switchOver) == HIGH) {
    if (digitalRead(switchOver) == HIGH && hotWater < 70 && ( ((hotWater < (bufferTop - 8) && hotWater < 60) || hotWater < 40) || bufferTop > 88)) {
      digitalWrite(hotWaterValve, LOW);
    }
    else {
      digitalWrite(hotWaterValve, HIGH);
    }
  }
  if (digitalRead(switchOver) == LOW) {
    if (digitalRead(switchOver) == LOW && hotWater < 44) {
      digitalWrite(hotWaterValve, LOW);
    }
    else if (digitalRead(hotWaterValve == LOW) && hotWater > 46 ) {
      digitalWrite(hotWaterValve, HIGH);
    }
  }
  //********************************************************************LCD DISPLAY*******************************************************************************
  switch (count) {
    case 0:
      lcd.clear();
      lcd.print("Boiler Temp"); lcd.setCursor(0, 1); lcd.print(boilerTemp); lcd.print(" C");
      j++;
      break;
    case 1:
      lcd.clear();
      lcd.print("Flue Gas"); lcd.setCursor(0, 1); lcd.print(flueGas); lcd.print(" C");
      j++;
      break;
    case 2:
      lcd.clear();
      lcd.print("Buffer Top"); lcd.setCursor(0, 1); lcd.print(bufferTop); lcd.print(" C");
      j++;
      break;
    case 3:
      lcd.clear();
      lcd.print("Buffer Mid"); lcd.setCursor(0, 1); lcd.print(bufferMid); lcd.print(" C");
      j++;
      break;
    case 4:
      lcd.clear();
      lcd.print("Buffer Bottom"); lcd.setCursor(0, 1); lcd.print(bufferBottom); lcd.print(" C");
      j++;
      break;
    case 5:
      lcd.clear();
      lcd.print("Hot Water"); lcd.setCursor(0, 1); lcd.print(hotWater); lcd.print(" C");
      j++;
      break;
    case 6:
      lcd.clear();
      lcd.print("I"); lcd.setCursor(0, 1); lcd.print(i); lcd.print(" C");
      j++;
      break;
    case 7:
      lcd.clear();
      lcd.print("I"); lcd.setCursor(0, 1); lcd.print(i); lcd.print(" C");
      j++;
      break;
    default:
      lcd.clear();
      lcd.print("ERROR");
      j = 0;
      break;
  }

  if (y > 10) {
    Serial.flush();
    Serial.println(String(flueGas) + "," + String(boilerTemp) + "," + String(bufferTop) + "," + String(bufferMid) + "," + String(hotWater) +
                   "," + String(bufferBottom) + "," + String(heartBeat) + "," + String(digitalRead(woodFan)) + "," + String(digitalRead(woodCircPump)) + "," + String(digitalRead(woodHeatCircPump)) +
                   "," + String(digitalRead(oilBoiler)) + "," + String(digitalRead(hotWaterValve)) + "," + String(digitalRead(switchOver)) + "," + String(digitalRead(startButton)));

    y = 0;
  }
  y++;

  delay(50);
}
