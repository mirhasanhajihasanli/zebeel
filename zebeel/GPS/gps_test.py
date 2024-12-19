import serial
import time
import json

# GPS Seri Port Ayarı
gps_ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

# Son geçerli GPS verisini saklamak için
last_valid_gps = {"latitude": "No GPS Fix", "longitude": "No GPS Fix"}

def parse_gps_data(line):
    """GPS verilerini ayrıştır ve JSON formatına dönüştür."""
    if line.startswith("$GPGGA"):
        data = line.split(',')
        fix_status = data[6]  # GPS Fix durumu
        if fix_status in ['1', '2']:  # 1: GPS Fix, 2: DGPS Fix
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
    """GPS modülünden veri al ve fix durumunu kontrol et."""
    global last_valid_gps
    try:
        line = gps_ser.readline().decode('ascii', errors='replace').strip()
        gps_data = parse_gps_data(line)
        if gps_data:
            # Geçerli bir GPS fix varsa veriyi sakla
            last_valid_gps = gps_data
            return gps_data
        else:
            # No GPS Fix durumunda son geçerli veriyi döndür
            print("No GPS Fix, using last valid data.")
            return last_valid_gps
    except Exception as e:
        print(f"GPS okuma hatası: {e}")
        return last_valid_gps

try:
    while True:
        # GPS Verilerini Oku
        gps_data = read_gps()
        print(json.dumps(gps_data, indent=4))
        time.sleep(2)  # GPS verilerini okuma aralığı

except KeyboardInterrupt:
    print("Program sonlandırılıyor...")
    gps_ser.close()

