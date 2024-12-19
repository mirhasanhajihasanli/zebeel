

import RPi.GPIO as GPIO
import spidev
import time
import csv

# Pin Tanımlamaları
NSS_PIN = 8
RESET_PIN = 25

# CSV Dosyası
CSV_FILE = "data_log.csv"

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(NSS_PIN, GPIO.OUT)
    GPIO.setup(RESET_PIN, GPIO.OUT)
    GPIO.output(NSS_PIN, GPIO.HIGH)
    GPIO.output(RESET_PIN, GPIO.HIGH)

def clean_message(raw_message):
    """Mesajı temizler ve <START> ile <END> arasında olan kısmı döndürür."""
    if "<START>" in raw_message and "<END>" in raw_message:
        start = raw_message.find("<START>") + len("<START>")
        end = raw_message.find("<END>")
        return raw_message[start:end]
    return None

def receive_message(spi):
    GPIO.output(NSS_PIN, GPIO.LOW)
    data = spi.xfer2([0x00] * 32)
    GPIO.output(NSS_PIN, GPIO.HIGH)
    raw_message = ''.join(chr(byte) for byte in data if 31 < byte < 127).strip()
    return clean_message(raw_message)

def save_to_csv(data):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def main():
    setup()
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1000000

    # CSV Başlığı yaz
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Mesafe (cm)", "Enlem", "Boylam", "Zaman Damgası"])

    try:
        while True:
            print("Mesaj bekleniyor...")
            message = receive_message(spi)
            if message:
                print(f"Alınan mesaj: {message}")
                try:
                    distance, lat, lon = message.split(",")
                    distance = distance.split(":")[1].replace("cm", "")
                    lat = lat.split(":")[1]
                    lon = lon.split(":")[1]
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

                    # Verileri kaydet
                    save_to_csv([distance, lat, lon, timestamp])
                except Exception as e:
                    print(f"Veri işleme hatası: {e}")
            else:
                print("Mesaj alınmadı.")
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        spi.close()

if __name__ == "__main__":
    main()
