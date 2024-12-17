

import RPi.GPIO as GPIO
import spidev
import time
import csv

# LoRa Ayarları
NSS_PIN = 8
RESET_PIN = 25
SPI_CHANNEL = 0
SPI_DEVICE = 0
CSV_FILE = 'lora_data.csv'

# GPIO Ayarları
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(NSS_PIN, GPIO.OUT)
    GPIO.setup(RESET_PIN, GPIO.OUT)
    GPIO.output(NSS_PIN, GPIO.HIGH)
    GPIO.output(RESET_PIN, GPIO.HIGH)

# LoRa Mesaj Alma
def receive_message(spi):
    GPIO.output(NSS_PIN, GPIO.LOW)
    data = spi.xfer2([0x00] * 256)  # 32 byte veri oku
    GPIO.output(NSS_PIN, GPIO.HIGH)
    raw_message = ''.join(chr(byte) for byte in data if 31 < byte < 127).strip()
    if "<START>" in raw_message and "<END>" in raw_message:
        start = raw_message.find("<START>") + len("<START>")
        end = raw_message.find("<END>")
        return raw_message[start:end]
    return None

# Veriyi Ayrıştır ve CSV'ye Kaydet
def save_to_csv(data):
    try:
        fields = ['Distance', 'Lat', 'Lon', 'Status']
        with open(CSV_FILE, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            # Eğer dosya boşsa başlık ekle
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(data)
            print(f"CSV'ye kaydedildi: {data}")
    except Exception as e:
        print(f"CSV kaydetme hatası: {e}")

# Mesaj Ayrıştırma
def parse_message(message):
    try:
        parts = message.split(',')
        distance = int(parts[0].split(':')[1].replace('cm', ''))
        latitude = float(parts[1].split(':')[1])
        longitude = float(parts[2].split(':')[1])
        status = "Full" if distance < 20 else "Medium" if distance < 50 else "Empty"
        return {
            'Distance': distance,
            'Lat': latitude,
            'Lon': longitude,
            'Status': status
        }
    except Exception as e:
        print(f"Mesaj ayrıştırma hatası: {e}")
        return None

# Ana Döngü
def main():
    setup()
    spi = spidev.SpiDev()
    spi.open(SPI_CHANNEL, SPI_DEVICE)
    spi.max_speed_hz = 1000000

    try:
        while True:
            print("Mesaj bekleniyor...")
            raw_message = receive_message(spi)
            if raw_message:
                print(f"Alınan ham mesaj: {raw_message}")
                parsed_data = parse_message(raw_message)
                if parsed_data:
                    save_to_csv(parsed_data)
            else:
                print("Mesaj alınmadı.")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Çıkış yapılıyor...")
        GPIO.cleanup()
        spi.close()

if __name__ == "__main__":
    main()
