from machine import Pin
from umqtt.simple import MQTTClient
import time

# LED ya configurado en boot.py
led = Pin(2, Pin.OUT)

# MQTT
MQTT_BROKER = "192.168.156.11"  # IP de tu PC donde corre Mosquitto
MQTT_PORT = 1883
MQTT_TOPIC = b"esp32/led"
CLIENT_ID = "esp32_client"

def mqtt_callback(topic, msg):
    print('Mensaje:', msg)
    if msg == b"on":
        led.on()
        print("LED ON")
    elif msg == b"off":
        led.off()
        print("LED OFF")

def main():
    try:
        client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        client.set_callback(mqtt_callback)
        client.connect()
        print('MQTT Conectado')
        
        client.subscribe(MQTT_TOPIC)
        print('Suscrito a:', MQTT_TOPIC)
        
        while True:
            client.check_msg()
            time.sleep(0.1)
            
    except Exception as e:
        print('Error:', e)
        time.sleep(5)
        main()  # Reintentar conexión

# Iniciar programa
if __name__ == '__main__':
    main()