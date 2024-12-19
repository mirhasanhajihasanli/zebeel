

import RPi.GPIO as GPIO
import time

# Pin tanımlamaları
TRIG_PIN = 23
ECHO_PIN = 24
GREEN_LED = 17
RED_LED = 22

# Başlangıç durumları
green_blink = False  # Yeşil LED yanıp sönme durumu
last_blink_time = 0  # Son yanıp sönme zamanı

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.setup(GREEN_LED, GPIO.OUT)
    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.output(TRIG_PIN, GPIO.LOW)
    print("Sensör başlatılıyor...")
    time.sleep(2)

def measure_distance():
    # Trigger sinyali gönder
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Echo yanıtını dinle
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        start_time = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        end_time = time.time()

    # Mesafeyi hesapla
    duration = end_time - start_time
    distance = (duration * 34300) / 2  # Ses hızı: 343 m/s
    return distance

def control_leds(distance):
    global green_blink, last_blink_time

    # Tüm LED'leri kapat
    GPIO.output(GREEN_LED, GPIO.LOW)
    GPIO.output(RED_LED, GPIO.LOW)

    if distance > 50:  # Boş
        GPIO.output(GREEN_LED, GPIO.HIGH)
        green_blink = False
    elif 20 < distance <= 50:  # Orta seviye
        current_time = time.time()
        if current_time - last_blink_time >= 5:  # 5 saniyede bir yanıp söner
            green_blink = not green_blink
            last_blink_time = current_time
        GPIO.output(GREEN_LED, GPIO.HIGH if green_blink else GPIO.LOW)
    else:  # Dolu
        GPIO.output(RED_LED, GPIO.HIGH)

def main():
    setup()
    try:
        while True:
            distance = measure_distance()
            print(f"Ölçülen Mesafe: {distance:.2f} cm")
            control_leds(distance)
            time.sleep(0.1)  # 0.1 saniye döngü süresi
    except KeyboardInterrupt:
        print("\nÇıkış yapılıyor...")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
