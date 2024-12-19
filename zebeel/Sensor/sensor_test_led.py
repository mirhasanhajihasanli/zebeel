

import RPi.GPIO as GPIO
import time

# Pin tanımlamaları
TRIG = 23  # TRIG pini GPIO23 (Pin 16)
ECHO = 24  # ECHO pini GPIO24 (Pin 18)
GREEN_LED = 17  # Yeşil LED GPIO17 (Pin 11)
RED_LED = 27  # Kırmızı LED GPIO27 (Pin 13)
BUZZER = 22  # Buzzer GPIO22 (Pin 15)

# GPIO ayarları
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

# Mesafe ölçüm fonksiyonu
def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10µs sinyal gönderilir
    GPIO.output(TRIG, False)

    start_time = time.time()
    end_time = time.time()

    # TRIG sinyali gönderildikten sonra ECHO'nun yükselmesini bekle
    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    # ECHO sinyali düştüğünde zamanı kaydet
    while GPIO.input(ECHO) == 1:
        end_time = time.time()

    # Mesafeyi hesapla
    duration = end_time - start_time
    distance = (duration * 34300) / 2  # cm cinsinden
    return distance

try:
    while True:
        # Mesafeyi ölç
        distance = measure_distance()
        print(f"Mesafe: {distance:.2f} cm")

        # Hatalı ölçümleri filtrelemek için kontrol ekleyin
        if distance < 2 or distance > 400:  # Geçersiz mesafeler
            print("Hatalı ölçüm! Mesafe algılanamadı.")
            GPIO.output(RED_LED, True)
            GPIO.output(GREEN_LED, False)
            GPIO.output(BUZZER, False)  # Buzzer kapalı
        elif distance < 20:  # Tam dolu kabul et
            print("Tam dolu! Buzzer etkin.")
            GPIO.output(RED_LED, True)  # Kırmızı LED sabit yanar
            GPIO.output(GREEN_LED, False)
            GPIO.output(BUZZER, True)  # Buzzer aktif
        elif 20 <= distance < 50:  # Orta doluluk
            print("Orta doluluk seviyesi!")
            GPIO.output(GREEN_LED, False)
            GPIO.output(BUZZER, False)  # Buzzer kapalı

            # Kırmızı LED her 3 saniyede bir yanıp söner
            GPIO.output(RED_LED, GPIO.HIGH)
            time.sleep(0.25)
            GPIO.output(RED_LED, GPIO.LOW)
            time.sleep(0.25)
        else:  # Boş kabul edilir
            GPIO.output(RED_LED, False)
            GPIO.output(GREEN_LED, True)
            GPIO.output(BUZZER, False)  # Buzzer kapalı

        time.sleep(0.5)  # Genel döngü gecikmesi

except KeyboardInterrupt:
    print("Çıkış yapılıyor...")
    GPIO.cleanup()
