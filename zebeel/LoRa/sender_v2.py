import RPi.GPIO as GPIO
import spidev
import time

NSS_PIN = 8
RESET_PIN = 25
DIO0_PIN = 19
MESSAGE = "<START>Merhaba LoRa!<END>"

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(NSS_PIN, GPIO.OUT)
    GPIO.setup(RESET_PIN, GPIO.OUT)
    GPIO.output(NSS_PIN, GPIO.HIGH)
    GPIO.output(RESET_PIN, GPIO.HIGH)

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

    try:
        while True:
            send_message(spi, MESSAGE)
            time.sleep(5)
    except KeyboardInterrupt:
        GPIO.cleanup()
        spi.close()

if __name__ == "__main__":
    main()
