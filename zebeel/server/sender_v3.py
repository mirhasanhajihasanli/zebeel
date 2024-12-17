

import RPi.GPIO as GPIO
import spidev
import time
import serial

# Pin Tanımlamaları
TRIG = 23
ECHO = 24
NSS_PIN = 8
RESET_PIN = 25

# GPS Ayarları
GPS_PORT = "/dev/ttyS0"
GPS_BAUDRATE = 9600

# Son geçerli GPS verileri için global değişkenler
last_latitude = 0.0
last_longitude = 0.0

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(NSS_PIN, GPIO.OUT)
    GPIO.setup(RESET_PIN, GPIO.OUT)
    GPIO.output(NSS_PIN, GPIO.HIGH)
    GPIO.output(RESET_PIN, GPIO.HIGH)

def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    end_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    while GPIO.input(ECHO) == 1:
        end_time = time.time()

    duration = end_time - start_time
    distance = int((duration * 34300) / 2)  # Integer olarak hesapla
    return distance

def read_gps(gps_serial):
    global last_latitude, last_longitude
    line = gps_serial.readline().decode('utf-8', errors='ignore')
    if "$GPGGA" in line:
        parts = line.split(',')
        try:
            latitude = float(parts[2]) / 100.0
            longitude = float(parts[4]) / 100.0
            last_latitude = round(latitude, 2)
            last_longitude = round(longitude, 2)
        except (ValueError, IndexError):
            pass
    return last_latitude, last_longitude

def send_message(spi, message):
    GPIO.output(NSS_PIN, GPIO.LOW)
    data = [0x80] + [ord(char) for char in message]
    spi.xfer2(data)
    GPIO.output(NSS_PIN, GPIO.HIGH)
    print(f"Mesaj gönderildi: {message}")

def main():
    setup()
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1000000

    gps_serial = serial.Serial(GPS_PORT, baudrate=GPS_BAUDRATE, timeout=1)

    try:
        while True:
            distance = measure_distance()
            latitude, longitude = read_gps(gps_serial)

            # Doluluk durumuna göre Status
            status = "F" if distance < 20 else "M" if distance < 50 else "E"

            # Mesaj oluştur
            message = f"<START>D:{distance},L:{latitude:.2f},Ln:{longitude:.2f},S:{status}<END>"
            send_message(spi, message)
            time.sleep(2)
    except KeyboardInterrupt:
        GPIO.cleanup()
        spi.close()
        gps_serial.close()

if __name__ == "__main__":
    main()
