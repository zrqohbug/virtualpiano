/* Program: stick_wifi
 *  
 * Designed by: Jie Huang & Runqiu Zhu
 * 
 * Description: This program is designed to implement ESP8266 WiFi 
 * Module and BNO055 Absolute Orientation Sensor on the Teensy 3.2. 
 * The goal is to collect data from the sensor and transmit it 
 * through UPD when receiving signal from the Raspberry Pi.Here, 
 * we have already setup a hotspot on Raspberry Pi. What we have 
 * to do is to connect the device to the Raspberry Pi, wait the 
 * device to receive signal 'w' from RPI and send the maxima sensor 
 * from the FIFO buffer.*/
#include <Wire.h>
#include <Adafruit_Sensor.h> 
#include <Adafruit_BNO055.h>
#include <Adafruit_ESP8266.h>
#include <utility/imumaths.h>
#include <FlexiTimer2.h>
#include <QueueArray.h>

/************************ WiFi Part ************************/
#define WIFI_Serial Serial2                // WIFI Port
#define  WIFI_SSID  "jh2674_rz373_AP"      // Network Name
#define  WIFI_PASS  "31415926"             // Network Password
#define HOST       "192.168.4.1"           // Host Address
#define PORT       8080                    // Host Port
#define myPORT     9008                    // Device Port

Adafruit_ESP8266 esp8266 = Adafruit_ESP8266(&WIFI_Serial,&USB_Serial,-1);

/************************ Sensor Part ************************/
Adafruit_BNO055 bno = Adafruit_BNO055(55);  // BNO55 Sensor Instance

float temp;
float accelz;
int accel_max;
String accel = "";
int data_length = 0;
int fifo_vol = 20;
int count_fifo = 0;

/************************ Status Led & Buttons ************************/
const int led = 13;
const int rbutton = 5;
const int lbutton = 20;
const int fbutton = 6;
volatile unsigned long triggertime = 0;
volatile unsigned long delta = 200;
int buttonflag = 2;

/************************ Data Collect and Process ************************/
int a = 0;
int incomingByte = 0;   // for incoming serial data
int countw = 0;
int countData = 0;
QueueArray <int> dataQueue;

/************************ For Debug Purpose ************************/
#define USB_Serial Serial                  // USB Port

void setup() {
  char buffer[50];
  
  // Flash LED On Power-up
  pinMode(led, OUTPUT);
  for(uint8_t i=0; i<3; i++) {
    digitalWrite(13, HIGH); delay(50);
    digitalWrite(13, LOW);  delay(100);
  }
    
/************************ Setup BNO55 Sensor ************************/  
  if(!bno.begin())  {    /* There was a problem detecting the BNO055 ... check your connections */    
    USB_Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");    
    while(1);  
  }  
  bno.setExtCrystalUse(true); 

/************************ Setup WiFi ************************/ 
  USB_Serial.begin(9600);         // Setup PC to Teensy serial
  WIFI_Serial.begin(115200);        // Setup Teensy to ESP8266 serial 

  /* Testing with AT */
  USB_Serial.println(F("Stick Testing!"));
  USB_Serial.print(F("Checking Respond..."));
  esp8266.println(F("AT"));
  if(esp8266.readLine(buffer, sizeof(buffer))) {
    USB_Serial.println(buffer);
    esp8266.find(); // Discard the 'OK' that follows
  } 
  else {
    USB_Serial.println(F("Respond Error"));
  }

  /* Connecting WiFi */
  USB_Serial.print(F("Connecting WiFi..."));
  esp8266.print("AT+CWJAP=\"");
  esp8266.print(F(WIFI_SSID));
  esp8266.print(F("\",\""));
  esp8266.print(F(WIFI_PASS));
  esp8266.println(F("\""));
  if(esp8266.readLine(buffer, sizeof(buffer))) {
    USB_Serial.println(buffer);
    esp8266.find(); // Discard the 'OK' that follows
  } 
  else {
    USB_Serial.println(F("Connect Error"));
  }

  /* Setup UDP Communication */
  unsigned long time = millis() +4000;
  while(millis() < time) {
  }
  USB_Serial.print(F("Connecting to UDP..."));
  esp8266.print("AT+CIPSTART=\"UDP\",\"");
  esp8266.print(F(HOST));
  esp8266.print("\",");
  esp8266.print(PORT);
  esp8266.print(",");
  esp8266.print(myPORT);
  esp8266.print(",");
  esp8266.println("0");
  if(esp8266.readLine(buffer, sizeof(buffer))) {
    USB_Serial.println(buffer);
    esp8266.find(); // Discard the 'OK' that follows
  } 
  else {
    USB_Serial.println(F("UDP Error"));
  }  
  
  /************************ Setup Buttons ************************/  
  pinMode(rbutton, INPUT_PULLUP);
  pinMode(lbutton, INPUT_PULLUP);
  pinMode(fbutton, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(rbutton), rightPress, FALLING);
  attachInterrupt(digitalPinToInterrupt(lbutton), leftPress, FALLING);
  attachInterrupt(digitalPinToInterrupt(fbutton), fullPress, FALLING);

  /************************ Setup Timer ************************/ 
  FlexiTimer2::set(10, 1.0/1000, event_dataCollect);
  FlexiTimer2::start();  
}

void loop() {
  // Indicate Idle Status
  digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)

  if (WIFI_Serial.available() > 0) {
     // read the incoming byte:
    incomingByte = WIFI_Serial.read();
    if (incomingByte == 119) {
      countw ++;
      if (countw == 1) {
        countw = 0;
        USB_Serial.print("I received: w");
        selectData();
        accel = String(accel_max)+String(buttonflag);
        data_length = accel.length();
        //USB_Serial.write(WIFI_Serial.read());
        WIFI_Serial.println("AT+CIPSEND="+String(data_length));
        delay(2);
        WIFI_Serial.println(accel);
        USB_Serial.println(accel);
      }
    }
  }
  /* For Setup WiFi Manually
 if ( USB_Serial.available() ) {
    WIFI_Serial.write( USB_Serial.read() );
  }
 if ( WIFI_Serial.available() ) {
    USB_Serial.println( WIFI_Serial.read() );
  }*/
}

void event_dataCollect()  { 
  accelz = sendAccel();
  int acce = accelz;
  dataQueue.push(acce);
  count_fifo ++;
  if( count_fifo > fifo_vol)
    dataQueue.pop();
}

void selectData() {
  float max_1 = 0;
    for(int i = 0;i < dataQueue.count(); i++)
    {
      if (max_1 < dataQueue.getNumber(i))
        max_1 = dataQueue.getNumber(i);
    }
    accel_max = max_1;
}

float sendAccel() {
  sensors_event_t event;
  bno.getAccel(&event); 
  float accel2, accelx2, accely2, accelz2;
  accelx2 = event.acceleration.x * event.acceleration.x;
  accely2 = event.acceleration.y * event.acceleration.y;
  accelz2 = event.acceleration.z * event.acceleration.z;
  accel2 = (accelx2 + accely2 + accelz2)/3;
  return accel2;
}

void rightPress() {
  if (millis() - triggertime > delta)
  { 
    triggertime =millis();
    USB_Serial.println("Button_R pressed!!!");
    if(buttonflag < 3) {
      buttonflag = buttonflag + 1;
    }
  }
}

void leftPress() {
  if (millis() - triggertime > delta)
  { 
    triggertime =millis();
    USB_Serial.println("Button_L pressed!!!");
    if (buttonflag >= 1) {
      buttonflag = buttonflag - 1;
    }
  }
}

void fullPress() {
  if (millis() - triggertime > delta)
  { 
    triggertime =millis();
    USB_Serial.println("Button_F pressed!!!");
    buttonflag = 5;
    }
}
