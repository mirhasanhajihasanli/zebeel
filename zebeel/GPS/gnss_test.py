import serial

try:
    ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
    print("GPS modülü bağlandı, veri bekleniyor...")

    while True:
        line = ser.readline()
        if line:
            print(line.decode('ascii', errors='ignore').strip())

except Exception as e:
    print(f"Hata: {e}")
finally:
    ser.close()
