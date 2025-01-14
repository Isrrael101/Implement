import cv2
import mediapipe as mp
import paho.mqtt.client as mqtt
import mysql.connector
from datetime import datetime
import urllib.request
import numpy as np

# MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# MQTT
MQTT_BROKER = "192.168.156.11"
MQTT_PORT = 1883
MQTT_TOPIC = "esp32/led"

# IP Webcam
IPWEBCAM_URL = "http://192.168.156.89:8080/shot.jpg"

# MySQL
DB_CONFIG = {
    'host': '192.168.156.11',
    'user': 'root',
    'password': '123456',
    'database': 'basedatos'
}

def get_frame_from_ip_webcam():
    try:
        img_resp = urllib.request.urlopen(IPWEBCAM_URL)
        img_arr = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        # Reducir el tamaño de la imagen a la mitad
        height, width = img.shape[:2]
        img = cv2.resize(img, (width//2, height//2))
        return True, img
    except Exception as e:
        print(f"Error IP Webcam: {e}")
        return False, None

def mqtt_connect():
    client = mqtt.Client()
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print("MQTT conectado")
        return client
    except Exception as e:
        print(f"Error MQTT: {e}")
        return None

def registrar_evento(estado, tipo_deteccion):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "INSERT INTO led_eventos (estado, deteccion_tipo) VALUES (%s, %s)"
        cursor.execute(query, (estado, tipo_deteccion))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error DB: {e}")

def detectar_pulgar(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y
    return thumb_tip < thumb_ip

def main():
    client = mqtt_connect()
    if not client:
        return

    led_estado = "APAGADO"
    
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        
        while True:
            success, image = get_frame_from_ip_webcam()
            if not success:
                continue

            # Voltear la imagen antes de procesarla
            image = cv2.flip(image, 1)

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Texto reducido y reposicionado
            texto = f"LED: {led_estado}"
            cv2.putText(image, texto, (26, 41), 
                       cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 2)
            cv2.putText(image, texto, (25, 40), 
                       cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 1)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
                    
                    pulgar_arriba = detectar_pulgar(hand_landmarks)
                    
                    if pulgar_arriba and led_estado == "APAGADO":
                        client.publish(MQTT_TOPIC, "on")
                        led_estado = "ENCENDIDO"
                        registrar_evento(led_estado, "pulgar_arriba")
                    elif not pulgar_arriba and led_estado == "ENCENDIDO":
                        client.publish(MQTT_TOPIC, "off")
                        led_estado = "APAGADO"
                        registrar_evento(led_estado, "pulgar_abajo")

            cv2.imshow('Control LED', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break

    cv2.destroyAllWindows()
    client.disconnect()

if __name__ == '__main__':
    main()