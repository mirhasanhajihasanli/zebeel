import serial

gps_serial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

try:
    while True:
        data = gps_serial.readline().decode('ascii', errors='ignore')
        if data:
            print(data.strip())
except KeyboardInterrupt:
    print("Çıkış yapılıyor...")