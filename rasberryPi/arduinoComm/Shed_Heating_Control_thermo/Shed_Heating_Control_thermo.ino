// this example is public domain. enjoy!
// www.ladyada.net/learn/sensors/thermocouple

#include "max6675.h"
#include <SoftwareSerial.h>

int BthermoDO = 7;
int BthermoCS = 6;
int BthermoCLK = 5;
int thermoDO = 17;
int thermoCS = 19;
int thermoCLK = 18;



MAX6675 thermocouple(thermoCLK, thermoCS, thermoDO);
MAX6675 Bthermocouple(BthermoCLK, BthermoCS, BthermoDO);

  
void setup() {
  Serial.begin(57600);//USB0
  // use Arduino pins 

  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
 // Serial.println("MAX6675 test");
  // wait for MAX chip to stabilize
  delay(500);
}

void loop() {
  // basic readout test, just print the current temp
  float boilerTemp = thermocouple.readCelsius();            //gasification boiler temp
  float flueGas = Bthermocouple.readCelsius();              //gasification flue temp.
  int boilerTempint = (int)boilerTemp;
  boilerTempint = boilerTempint+100;
  int flueGasint = (int)flueGas;
  flueGasint = flueGasint + 100;
  String var = String(boilerTempint);
  String var1 = String(flueGasint);
  String var2 = var + var1;



   
  // Serial.print("C = "); 
//Serial.println(boilerTemp);
//Serial.println(flueGas); 
//Serial.println( var2);
//Serial.write( flueGasint);
 // if (Serial.available())
      Serial.println(var2);
      delay(1000);
      Serial.flush();

}
