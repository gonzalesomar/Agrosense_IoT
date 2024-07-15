/*
 * LoRa E32-TTL-100
 * Start device or reset to send a message
 * https://mischianti.org
 *
 * E32-TTL-100----- Arduino UNO
 * M0         ----- GND
 * M1         ----- GND
 * TX         ----- PIN 2 (PullUP)
 * RX         ----- PIN 3 (PullUP & Voltage divider)
 * AUX        ----- Not connected
 * VCC        ----- 3.3v/5v
 * GND        ----- GND
 *
 */
#include "Arduino.h"
 
#include <SoftwareSerial.h>
String receivedData = ""; 
SoftwareSerial mySerial(3, 2); // e32 TX e32 RX
const int ec = 100;

const int SensON = A1;
const int Sens1 = A0;
const int Sens3 = A2;

const int StepUpON = 10;
const int ReEC = A3;

const int BatteryON = A4;
const int Battery = A5;

const int LoraON = 8;
const int Lora4 = 4;
const int Lora5 = 5;
const int Lora6 = 6;

const int AirValue = 780;
const int WaterValue = 280;

void setup() {
  Serial.begin(115200);
  delay(500);

  pinMode(SensON, OUTPUT);
  pinMode(Sens1, INPUT);
  pinMode(Sens3, INPUT);

  pinMode(StepUpON, OUTPUT);
  pinMode(ReEC, OUTPUT);

  pinMode(BatteryON, OUTPUT);
  pinMode(Battery, INPUT);

  pinMode(LoraON, OUTPUT);
  pinMode(Lora4, OUTPUT);
  pinMode(Lora5, OUTPUT); // Set PD5 as an output pin
  pinMode(Lora6, OUTPUT); // Set PD6 as an output pin 

  digitalWrite(SensON, LOW);

  digitalWrite(StepUpON, LOW);
  digitalWrite(ReEC, LOW);

  digitalWrite(BatteryON, LOW);

  digitalWrite(Lora4, HIGH);
  digitalWrite(Lora5, LOW); // Turn off PD5
  digitalWrite(Lora6, LOW); // Turn off PD6
  digitalWrite(LoraON, HIGH);
  Serial.println("Hi, I'm going to send message cutie!");
 
  mySerial.begin(9600);
  mySerial.println("Hello, world?");
}
 
void loop() {
  while (mySerial.available()) {
    char inChar = (char)mySerial.read();
    receivedData += inChar;
    // Check for end-of-line character to signify end of message
    if (inChar == 'A') {
      Serial.write("\n");
      Serial.print("Received from LoRa: ");
      Serial.print(receivedData);  // Print the complete message
      receivedData = "";  // Clear the string for new data
      char buffer[50]; // Adjust the size based on your needs
      // Convert readings to strings and concatenate them

      digitalWrite(StepUpON, HIGH);

      digitalWrite(SensON, HIGH);
      delay(10);
      int lectura1 = analogRead(Sens1);
      int lectura3 = analogRead(Sens3);
      digitalWrite(SensON, LOW);
      float lectura1_f = ((float)(AirValue - lectura1) / (float)(AirValue - WaterValue)) * 100.0;
      float lectura3_f = ((float)(AirValue - lectura3) / (float)(AirValue - WaterValue)) * 100.0;
      lectura1 = round(lectura1_f);
      lectura3 = round(lectura3_f);
      int lectura2 = (lectura1 + lectura3) / 2; // This will be an integer division

      digitalWrite(BatteryON, HIGH);
      delay(10);
      int nivelBateria = analogRead(Battery);
      // int nivelBateriaConvertido = (nivelBateria * 330) / 1024;
      digitalWrite(BatteryON, LOW);

      snprintf(buffer, sizeof(buffer), "%d %d %d %d %d.", nivelBateria, lectura1, lectura2, lectura3, ec);
      mySerial.write(buffer);    
    }
  }
}