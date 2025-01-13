ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- Crear tabla para registrar eventos del LED
CREATE TABLE IF NOT EXISTS led_eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estado VARCHAR(10) NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deteccion_tipo VARCHAR(50)
);