

import spidev
import RPi.GPIO as GPIO
from time import sleep

# LoRa Pin Tanımları
NSS_PIN = 8      # GPIO8 (SPI Chip Select)
RESET_PIN = 25   # GPIO25 (Reset Pin)
DIO0_PIN = 19    # GPIO19 (Interrupt)

# LoRa Register Tanımları
REG_FIFO = 0x00
REG_OP_MODE = 0x01
REG_FIFO_ADDR_PTR = 0x0D
REG_FIFO_TX_BASE_ADDR = 0x0E
REG_FIFO_RX_BASE_ADDR = 0x0F
REG_IRQ_FLAGS = 0x12
REG_RX_NB_BYTES = 0x13
REG_MODEM_CONFIG_1 = 0x1D
REG_MODEM_CONFIG_2 = 0x1E
REG_PAYLOAD_LENGTH = 0x22
REG_FIFO_RX_CURRENT_ADDR = 0x10

# Mod Ayarları
MODE_SLEEP = 0x00
MODE_STDBY = 0x01
MODE_TX = 0x03
MODE_RX_CONT = 0x05

class LoRa:
    def __init__(self):
        # SPI ve GPIO Kurulumu
        self.spi = spidev.SpiDev(0, 0)
        self.spi.max_speed_hz = 500000
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(NSS_PIN, GPIO.OUT)
        GPIO.setup(RESET_PIN, GPIO.OUT)
        GPIO.setup(DIO0_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.reset()

    def reset(self):
        """ LoRa modülünü resetler """
        GPIO.output(RESET_PIN, GPIO.LOW)
        sleep(0.1)
        GPIO.output(RESET_PIN, GPIO.HIGH)
        sleep(0.1)

    def write_register(self, address, value):
        """ LoRa register yazma """
        GPIO.output(NSS_PIN, GPIO.LOW)
        self.spi.xfer2([address | 0x80, value])
        GPIO.output(NSS_PIN, GPIO.HIGH)

    def read_register(self, address):
        """ LoRa register okuma """
        GPIO.output(NSS_PIN, GPIO.LOW)
        response = self.spi.xfer2([address & 0x7F, 0x00])
        GPIO.output(NSS_PIN, GPIO.HIGH)
        return response[1]

    def set_mode(self, mode):
        """ Çalışma modunu ayarla """
        self.write_register(REG_OP_MODE, mode)

    def send_message(self, message):
        """ Mesaj gönderimi """
        self.set_mode(MODE_STDBY)
        self.write_register(REG_FIFO_ADDR_PTR, self.read_register(REG_FIFO_TX_BASE_ADDR))
        for byte in message.encode('utf-8'):
            self.write_register(REG_FIFO, byte)
        self.write_register(REG_PAYLOAD_LENGTH, len(message))
        self.set_mode(MODE_TX)
        print(f"Mesaj gönderiliyor: {message}")
        while GPIO.input(DIO0_PIN) == 0:
            sleep(0.01)
        print("Mesaj gönderildi.")

    def receive_message(self):
        """ Mesaj alımı """
        self.set_mode(MODE_RX_CONT)
        print("Alım moduna geçildi. Mesaj bekleniyor...")
        while GPIO.input(DIO0_PIN) == 0:
            sleep(0.01)
        irq_flags = self.read_register(REG_IRQ_FLAGS)
        self.write_register(REG_IRQ_FLAGS, irq_flags)
        if irq_flags & 0x40:  # RX_DONE
            self.write_register(REG_FIFO_ADDR_PTR, self.read_register(REG_FIFO_RX_CURRENT_ADDR))
            payload_length = self.read_register(REG_RX_NB_BYTES)
            message = ""
            for _ in range(payload_length):
                message += chr(self.read_register(REG_FIFO))
            print(f"Gelen mesaj: {message}")
        else:
            print("Alım başarısız.")

    def cleanup(self):
        self.spi.close()
        GPIO.cleanup()
