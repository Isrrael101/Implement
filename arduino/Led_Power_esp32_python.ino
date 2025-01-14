#include <WiFi.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "FABRICA";
const char* password = "Carol2023@";

// MQTT Broker settings
const char* mqtt_broker = "192.168.0.101";
const int mqtt_port = 1883;zxc
const char* mqtt_topic = "esp32/led";
const char* client_id = "esp32_client";

// Pin definitions
const int ledPin = 2;  // Built-in LED on ESP32

// Initialize WiFi and MQTT clients
WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println("Connecting to WiFi...");
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  // Convert payload to string
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  Serial.print("Message received: ");
  Serial.println(message);
  
  // Control LED based on message
  if (message == "on") {
    digitalWrite(ledPin, HIGH);
    Serial.println("LED ON");
  }
  else if (message == "off") {
    digitalWrite(ledPin, LOW);
    Serial.println("LED OFF");
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.println("Attempting MQTT connection...");
    
    if (client.connect(client_id)) {
      Serial.println("MQTT Connected");
      client.subscribe(mqtt_topic);
      Serial.print("Subscribed to: ");
      Serial.println(mqtt_topic);
    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" Retrying in 5 seconds...");
      delay(5000);
    }
  }
}

void setup() {
  // Initialize serial communication
  Serial.begin(115200);
  
  // Configure LED pin
  pinMode(ledPin, OUTPUT);
  
  // Setup WiFi connection
  setup_wifi();
  
  // Configure MQTT broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  delay(100);
}