import RPi.GPIO as GPIO
import serial
import time
import json

# Pin ve Seri Port Ayarları
TRIG = 23
ECHO = 24
gps_ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

# LED Pinleri
GREEN_LED = 17  # Yeşil LED GPIO17
RED_LED = 27    # Kırmızı LED GPIO27

# GPIO Ayarları
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

# Son geçerli GPS verisi
last_valid_gps = {
    "latitude": "No GPS Fix",
    "longitude": "No GPS Fix",
    "fix_status": "0",
    "satellites": "0",
    "altitude": "N/A"
}

def parse_gps_data(line):
    if line.startswith("$GPGGA"):
        data = line.split(',')
        fix_status = data[6]
        if fix_status in ['1', '2']:  # Geçerli GPS Fix durumları
            latitude = data[2] + " " + data[3]
            longitude = data[4] + " " + data[5]
            satellites = int(data[7])
            altitude = float(data[9])
            return {
                "latitude": latitude,
                "longitude": longitude,
                "fix_status": fix_status,
                "satellites": satellites,
                "altitude": altitude
            }
    return None

def read_gps():
    """GPS verilerini oku ve geçerli fix varsa döndür, yoksa son geçerli veriyi kullan."""
    global last_valid_gps
    try:
        line = gps_ser.readline().decode('ascii', errors='replace').strip()
        gps_data = parse_gps_data(line)
        if gps_data:  # Eğer geçerli bir GPS fix alınmışsa
            last_valid_gps = gps_data
            return gps_data
        else:
            print("No GPS Fix, using last valid data.")
            return last_valid_gps
    except Exception as e:
        print(f"GPS okuma hatası: {e}")
        return last_valid_gps

def measure_distance():
    """Ultrasonik sensörle mesafeyi ölç."""
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2
    return distance

try:
    while True:
        # Mesafeyi ölç
        distance = measure_distance()
        if distance < 20:
            fill_level = "Full"
            GPIO.output(RED_LED, True)
            GPIO.output(GREEN_LED, False)
        elif distance < 50:
            fill_level = "Medium"
            GPIO.output(RED_LED, False)
            GPIO.output(GREEN_LED, False)
        else:
            fill_level = "Empty"
            GPIO.output(RED_LED, False)
            GPIO.output(GREEN_LED, True)

        # GPS verilerini oku
        gps_data = read_gps()

        # Verileri JSON formatında birleştir
        data = {
            "bin_id": "001",
            "latitude": gps_data["latitude"],
            "longitude": gps_data["longitude"],
            "fill_level": fill_level,
            "altitude": gps_data["altitude"],
            "satellites": gps_data["satellites"]
        }

        print(json.dumps(data, indent=4))
        time.sleep(2)

except KeyboardInterrupt:
    print("Program sonlandırılıyor...")
    GPIO.cleanup()
    gps_ser.close()
