from machine import Pin
import network
import time

# LED
led = Pin(2, Pin.OUT)

# WiFi
WIFI_SSID = "Redmi Note 13"
WIFI_PASSWORD = "carol123"

def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Conectando a:', WIFI_SSID)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            print('.', end='')
            time.sleep(0.5)
    
    print('\nConectado!')
    print('IP:', wlan.ifconfig()[0])
    return wlan.ifconfig()[0]

# Iniciar conexión WiFi
try:
    ip = wifi_connect()
    print('ESP32 listo en IP:', ip)
except Exception as e:
    print('Error de conexión:', e)