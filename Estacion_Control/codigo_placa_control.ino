/*
 * LoRa E32
 * Start device or reset to send a message
 * https://mischianti.org
 *
 * E32        ----- esp32
 * M0         ----- GND
 * M1         ----- GND
 * TX         ----- RX2 (PullUP)
 * RX         ----- TX2 (PullUP)
 * AUX        ----- Not connected
 * VCC        ----- 3.3v/5v
 * GND        ----- GND
 *
 */

#include "Arduino.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
unsigned long previousMillis = 0; // Stores the last time input was checked
const long interval = 1*1000;//40*1000; // Interval in milliseconds to check for input
String receivedData = "";
const int ledPin = 13; // Pin where the LED is connected



// Replace with your network credentials
const char* ssid = "redpucp";
const char* password = "C9AA28BA93";

// Server IP and port
const char* serverIP = "10.100.108.61";
const int serverPort = 9595;
const char* serverName = "http://10.100.108.61:9595/send-state/";

void parseStringToJSON(const String& dataString, DynamicJsonDocument& jsonDoc) {
  // Split the string into individual values
  float values[5];
  int index = 0;
  int start = 0;
  int end = dataString.indexOf(' ');
  while (end != -1 && index < 5) {
    values[index++] = dataString.substring(start, end).toFloat();
    start = end + 1;
    end = dataString.indexOf(' ', start);
  }
  values[index] = dataString.substring(start).toFloat();  // Last value

  // Fill the JSON document with the parsed values
  jsonDoc["battery_level"] = values[0];
  jsonDoc["humidity_25"] = values[1];
  jsonDoc["humidity_50"] = values[2];
  jsonDoc["humidity_75"] = values[3];
  jsonDoc["electrical_conductivity"] = values[4];
}

void setup() {


  Serial.begin(9600);
  pinMode(19, OUTPUT);
  pinMode(21, OUTPUT);
  pinMode(ledPin,OUTPUT);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi..");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to the WiFi network");
  delay(500);
  Serial.println("Hi, I'm going to send message!");
  Serial2.begin(9600);
  Serial2.println("Hello, world?");
}
 
void loop() {

  Serial.write("Iniciando................");
  Serial.write("\n");
  delay(1500);
  Serial.write("\n");
  Serial.write("Requesting information to ModuleA....");
  Serial2.write("A");
  Serial.write("\n");
  delay(1500);

  digitalWrite(19, LOW);
  digitalWrite(21, LOW);

  while (Serial2.available()) {
    char inChar = (char)Serial2.read();
    receivedData += inChar;
    // Check for end-of-line character to signify end of message
    if (inChar == '.') {
      Serial.print("Received from LoRa A: ");
      Serial.print(receivedData);  // Print the complete message
      //////////////////////////////////////////////////WiFI///////////////////////////////////////////
      if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
   
        // Construct the URL for the request
        String serverPath = String("http://") + serverIP + ":" + serverPort + "/Sensor1/";
   
        // Specify content-type header
        http.begin(serverPath.c_str());
        http.addHeader("Content-Type", "application/json");
   
 
        // Create a JSON object
        DynamicJsonDocument jsonDoc(256);
        parseStringToJSON(receivedData, jsonDoc);
     
        // Convert JSON object to string
        String jsonString;
        serializeJson(jsonDoc, jsonString);
   
   
        // Send HTTP POST request
        int httpResponseCode = http.POST(jsonString);
   
        // If you need to check the response
        if (httpResponseCode > 0) {
          String response = http.getString();  // Get the response to the request
          Serial.println(httpResponseCode);   // Print return code
          Serial.println(response);           // Print request answer
        } else {
          Serial.print("Error on sending POST: ");
          Serial.println(httpResponseCode);
        }
   
        // Free resources
        http.end();
      } else {
        Serial.println("WiFi Disconnected");
      }
      delay(1000);
      //////////////////////////////////////////////////////////////////////////////////////////////////
      receivedData = "";  // Clear the string for new data
    }
  }
  delay(1500);
  Serial.write("\n");
  Serial2.write("B");
  Serial.write("Requesting information to ModuleB....");
  Serial.write("\n");  


  delay(1500);
  while (Serial2.available()) {
    char inChar = (char)Serial2.read();
    receivedData += inChar;
    // Check for end-of-line character to signify end of message
    if (inChar == '.') {
      Serial.print("Received from LoRa B: ");
      Serial.print(receivedData);  // Print the complete message
      

      //////////////////////////////////////////////////WiFI///////////////////////////////////////////
      if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
   
        // Construct the URL for the request
        String serverPath = String("http://") + serverIP + ":" + serverPort + "/Sensor2/";
   
        // Specify content-type header
        http.begin(serverPath.c_str());
        http.addHeader("Content-Type", "application/json");

       

        // Create a JSON object
        DynamicJsonDocument jsonDoc(256);
        parseStringToJSON(receivedData, jsonDoc);

        // Convert JSON object to string
        String jsonString;
        serializeJson(jsonDoc, jsonString);
   
   
        // Send HTTP POST request
        int httpResponseCode = http.POST(jsonString);
   
        // If you need to check the response
        if (httpResponseCode > 0) {
          String response = http.getString();  // Get the response to the request
          Serial.println(httpResponseCode);   // Print return code
          Serial.println(response);           // Print request answer
        } else {
          Serial.print("Error on sending POST: ");
          Serial.println(httpResponseCode);
        }
   
        // Free resources
        http.end();
      } else {
        Serial.println("WiFi Disconnected");
      }
      delay(1000);
      //////////////////////////////////////////////////////////////////////////////////////////////////

     
      receivedData = "";  // Clear the string for new data
    }
  }

  Serial.print("Wait time..........");
  while(1){
    unsigned long currentMillis = millis(); // Get the current time

////////////////////////////////////////////////////////////////////
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;

      // Especifica la URL del servidor
      http.begin(serverName);
      
      // Envía la solicitud HTTP GET
      int httpResponseCode = http.GET();
      
      if (httpResponseCode > 0) {
        // Lee la respuesta del servidor
        String payload = http.getString();
        Serial.println(httpResponseCode);
        Serial.println(payload);
        
        // Reserva espacio suficiente para el JSON
        const size_t capacity = JSON_OBJECT_SIZE(1) + 20;
        DynamicJsonDocument doc(capacity);

        // Parsea la respuesta JSON
        DeserializationError error = deserializeJson(doc, payload);
        if (error) {
          Serial.print("Error al parsear JSON: ");
          Serial.println(error.c_str());
          return;
        }

        // Obtiene el valor booleano
        bool value = doc["state"];
        //Serial.println(doc);
        Serial.println("--------------");
        // Imprime el valor booleano
        Serial.print("Valor booleano recibido: ");

        Serial.println(value ? "true" : "false");
        
        // Controla el pin 13 según el valor booleano
        if (value) {
          digitalWrite(13, HIGH); // Enciende el pin 13
          Serial.print("ON");
        } else {
          digitalWrite(13, LOW); // Apaga el pin 13
          Serial.print("OFF");
        }
        
      } else {
        Serial.print("Error en la solicitud HTTP: ");
        Serial.println(httpResponseCode);
      }
      // Finaliza la conexión
      http.end();
    } else {
      Serial.println("Error de conexión Wi-Fi");
    }
    // Espera 10 segundos antes de realizar otra solicitud
    delay(1000);


////////////////////////////////////////////////////////////////////

    if (currentMillis - previousMillis >= interval) {
      Serial.print("Cumplio tiempo");
      previousMillis = currentMillis;
      break;
    }    
  }
  

}