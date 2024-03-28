
#ifdef ENABLE_DEBUG
  #define DEBUG_ESP_PORT Serial
  #define NODEBUG_WEBSOCKETS
  #define NDEBUG
#endif 

#include <Arduino.h>
#if defined(ESP8266)
  #include <ESP8266WiFi.h>
#elif defined(ESP32) || defined(ARDUINO_ARCH_RP2040)
  #include <WiFi.h>
#endif

#include "SinricPro.h"
#include "SinricProFanUS.h"

#define WIFI_SSID         "yogesh"    
#define WIFI_PASS         "geetesh1"
#define APP_KEY           "328200f4-9a7b-4473-be8b-c169c1706530"      // Should look like "de0bxxxx-1x3x-4x3x-ax2x-5dabxxxxxxxx"
#define APP_SECRET        "4238c44f-281d-493c-9082-2afc8bc14d87-549686a7-9ebc-439b-9eb8-724ba00a02d7"   // Should look like "5f36xxxx-x3x7-4x3x-xexe-e86724a9xxxx-4c4axxxx-3x3x-x5xe-x9x3-333d65xxxxxx"
#define FAN_ID            "65f84cf638f6f4a3cdc4aaff"    // Should look like "5dc1564130xxxxxxxxxxxxxx"
#define BAUD_RATE         115200             

// we use a struct to store all states and values for our fan
// fanSpeed (1..3)
struct {
  bool powerState = false;
  int fanSpeed = 1;
} device_state;

bool onPowerState(const String &deviceId, bool &state) {
  Serial.printf("Fan turned %s\r\n", state?"on":"off");
   digitalWrite(16,!(state));
    
      
  device_state.powerState = state;
  return true; // request handled properly
}

bool onRangeValue(const String &deviceId, int& rangeValue) {
  device_state.fanSpeed = rangeValue;
  Serial.printf("Fan speed changed to %d\r\n", device_state.fanSpeed);

  return true;
}


// Fan rangeValueDelta is from -3..+3
bool onAdjustRangeValue(const String &deviceId, int& rangeValueDelta) {
  device_state.fanSpeed += rangeValueDelta;
  Serial.printf("Fan speed changed about %i to %d\r\n", rangeValueDelta, device_state.fanSpeed);

  rangeValueDelta = device_state.fanSpeed; // return absolute fan speed
  return true;
}

void setupWiFi() {
  pinMode(16, OUTPUT);
  Serial.printf("\r\n[Wifi]: Connecting");
  
  #if defined(ESP8266)
    WiFi.setSleepMode(WIFI_NONE_SLEEP); 
    WiFi.setAutoReconnect(true);
  #elif defined(ESP32)
    WiFi.setSleep(false); 
    WiFi.setAutoReconnect(true);
  #endif
  
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.printf(".");
    delay(250);
  }
  Serial.printf("connected!\r\n[WiFi]: IP-Address is %s\r\n", WiFi.localIP().toString().c_str());
}

void setupSinricPro() {
  SinricProFanUS &myFan = SinricPro[FAN_ID];

  // set callback function to device
  myFan.onPowerState(onPowerState);
  myFan.onRangeValue(onRangeValue);
  myFan.onAdjustRangeValue(onAdjustRangeValue);

  // setup SinricPro
  SinricPro.onConnected([](){ Serial.printf("Connected to SinricPro\r\n"); }); 
  SinricPro.onDisconnected([](){ Serial.printf("Disconnected from SinricPro\r\n"); });
  SinricPro.begin(APP_KEY, APP_SECRET);
}

// main setup function
void setup() {
  Serial.begin(BAUD_RATE); Serial.printf("\r\n\r\n");
  setupWiFi();
  setupSinricPro();
}

void loop() {
  SinricPro.handle();
}