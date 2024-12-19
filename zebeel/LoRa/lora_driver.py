

import spidev
import RPi.GPIO as GPIO
import time

class LoRa:
    def __init__(self, nss_pin, reset_pin):
        self.nss_pin = nss_pin
        self.reset_pin = reset_pin

        # GPIO Ayarları
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.nss_pin, GPIO.OUT)
        GPIO.setup(self.reset_pin, GPIO.OUT)

        # SPI Ayarları
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 500000

        # Modül başlatma
        self.reset()

    def reset(self):
        GPIO.output(self.reset_pin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.reset_pin, GPIO.HIGH)
        time.sleep(0.1)

    def send(self, data):
        GPIO.output(self.nss_pin, GPIO.LOW)
        self.spi.xfer2([0x00] + list(data.encode()))
        GPIO.output(self.nss_pin, GPIO.HIGH)
        time.sleep(0.1)

    def receive(self):
        GPIO.output(self.nss_pin, GPIO.LOW)
        response = self.spi.xfer2([0x01] + [0x00] * 255)
        GPIO.output(self.nss_pin, GPIO.HIGH)
        # Gelen veriyi stringe çevir
        message = bytes([x for x in response if x != 0x00]).decode('utf-8', errors='ignore')
        return message.strip()

    def close(self):
        self.spi.close()
        GPIO.cleanup()
