# Guía de Instalación y Configuración del Sistema

## 1. Preparación del Entorno Virtual Python

```bash
# Crear directorio del proyecto
mkdir Implemen_01
cd Implemen_01

# Crear entorno virtual
python -m venv entorno

# Activar entorno virtual
# En Windows:
entorno\Scripts\activate
# En Linux/Mac:
source entorno/bin/activate
```

## 2. Instalación de Librerías Python
```bash
# Instalar librerías necesarias
pip install opencv-python
pip install mediapipe
pip install paho-mqtt
pip install mysql-connector-python
pip install numpy
```

## 3. Instalación de Mosquitto MQTT Broker

### En Windows:
```bash
# Usando chocolatey
choco install mosquitto

# Configurar Mosquitto
# Crear/editar archivo C:\Program Files\mosquitto\mosquitto.conf
listener 1883
allow_anonymous true

# Iniciar servicio
net start mosquitto
```

### En Linux:
```bash
sudo apt-get install mosquitto mosquitto-clients
sudo systemctl start mosquitto
```

## 4. Configuración del ESP32

### Instalar herramientas para ESP32:
```bash
pip install esptool
pip install rshell
```

### Instalar MicroPython en ESP32:
```bash
# Borrar flash
esptool.py --port COMX erase_flash

# Descargar firmware de MicroPython para ESP32 de:
# https://micropython.org/download/esp32/

# Flashear firmware
esptool.py --chip esp32 --port COMX --baud 460800 write_flash -z 0x1000 esp32-XXXXXXXX.bin
```

### Instalar módulos necesarios en ESP32:
```bash
# Conectar con rshell
rshell -p COMX

# Entrar al REPL
repl

# Instalar umqtt.simple
import upip
upip.install('micropython-umqtt.simple')
```

## 5. Estructura de Archivos
```
Implemen_01/
│
├── entorno/                  # Entorno virtual Python
│
├── esp32_code/              # Código para ESP32
│   ├── boot.py              # Configuración WiFi
│   └── main.py              # Lógica MQTT
│
└── py_laptop/               # Código Python para laptop
    └── vision.py            # Programa de visión artificial
```

## 6. Base de Datos MySQL

### Crear base de datos y tabla:
```sql
CREATE DATABASE basedatos;
USE basedatos;

CREATE TABLE led_eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estado VARCHAR(10) NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deteccion_tipo VARCHAR(50)
);
```

## 7. Configuración de IP Webcam

1. Instalar "IP Webcam" desde Google Play Store
2. Abrir la aplicación
3. Desplazarse hasta abajo
4. Tocar "Start server"
5. Anotar la URL mostrada

## 8. Pasos Finales

1. Cargar códigos al ESP32:
```bash
rshell -p COMX cp esp32_code/boot.py /pyboard/
rshell -p COMX cp esp32_code/main.py /pyboard/
```

2. Verificar Mosquitto:
```bash
# Terminal 1
mosquitto_sub -t esp32/led

# Terminal 2
mosquitto_pub -t esp32/led -m "on"
```

3. Iniciar el programa de visión:
```bash
python py_laptop/vision.py
```

## 9. Verificación de Funcionamiento

1. El ESP32 debe mostrar su IP al iniciar
2. IP Webcam debe estar accesible
3. Los gestos deben detectarse correctamente
4. El LED debe responder a los gestos
5. Los eventos deben registrarse en la base de datos

## 10. Solución de Problemas Comunes

1. Error de conexión MQTT:
   - Verificar que Mosquitto está corriendo
   - Comprobar firewall
   - Verificar IP correcta

2. Error de conexión ESP32:
   - Verificar puerto COM
   - Reintentar conexión rshell
   - Verificar credenciales WiFi

3. Error de IP Webcam:
   - Verificar que el teléfono está en la misma red
   - Comprobar URL correcta
   - Verificar puerto 8080 accesible

4. Error de MySQL:
   - Verificar servicio activo
   - Comprobar credenciales
   - Verificar existencia de tabla
