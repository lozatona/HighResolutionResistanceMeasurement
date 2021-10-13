#include <SPI.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Test");

  SPI.begin();
  delay(10);
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
  delay(10);

  //Get the device ID
  //Ask for ID
  byte CommRegWrite=0x40;    //instruction for reading 
  byte CommOut=CommRegWrite|0x05; //adress of ID register
  Serial.println(CommOut,BIN);
  SPI.transfer(CommOut);    //transmit the data to device - write in device/slave 
  delayMicroseconds(1);
  byte answer=SPI.transfer(0xFF); //reading instruction 
  Serial.println(answer,HEX);
  Serial.println("Finished");
}

void loop() {
  // put your main code here, to run repeatedly:
}
