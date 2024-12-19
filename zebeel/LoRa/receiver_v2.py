import RPi.GPIO as GPIO
import spidev
import time

NSS_PIN = 8
RESET_PIN = 25
DIO0_PIN = 19

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(NSS_PIN, GPIO.OUT)
    GPIO.setup(RESET_PIN, GPIO.OUT)
    GPIO.output(NSS_PIN, GPIO.HIGH)
    GPIO.output(RESET_PIN, GPIO.HIGH)

def receive_message(spi):
    GPIO.output(NSS_PIN, GPIO.LOW)
    data = spi.xfer2([0x00] * 32)  # 0x00 okuma komutu
    GPIO.output(NSS_PIN, GPIO.HIGH)
    message = ''.join(chr(byte) for byte in data if byte != 0x00)
    return message.strip()

def main():
    setup()
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1000000

    try:
        while True:
            print("Mesaj bekleniyor...")
            message = receive_message(spi)
            if message:
                print(f"Alınan mesaj: {message}")
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        spi.close()

if __name__ == "__main__":
    main()
