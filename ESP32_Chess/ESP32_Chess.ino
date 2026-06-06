#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <LittleFS.h>

/* Put your SSID & Password */
const char* ssid = "ESP_Domeniconi"; // Enter SSID here
const char* password = "12345678"; //Enter Password here
/* Put IP Address details */
IPAddress local_ip(192,168,1,1);
IPAddress gateway(192,168,1,1);
IPAddress subnet(255,255,255,0);
AsyncWebServer server(80);

void setup() {


  // Begin LittleFS
  if (!LittleFS.begin())
  {
    Serial.println("An Error has occurred while mounting LittleFS");
    return;
  }

  Serial.begin(115200);

  WiFi.softAP(ssid, password);
  WiFi.softAPConfig(local_ip, gateway, subnet);
  delay(100); 

  server.on("/move.html", HTTP_GET, [](AsyncWebServerRequest *request){
    const AsyncWebParameter* p = request->getParam(0);
    const AsyncWebParameter* p1 = request->getParam(1);
      
    Serial.println("move," + p->value() + "," + p1->value());
    request->send(200, "text/plain", "message received");
  });
  


  server.serveStatic("/", LittleFS, "/").setDefaultFile("chess.html");
  server.begin();
  Serial.println("HTTP server started");
}
void loop() {}
