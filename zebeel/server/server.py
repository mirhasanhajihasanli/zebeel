

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import csv

app = Flask(__name__)
socketio = SocketIO(app)

# Verileri saklamak için bir global liste
data_storage = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data_storage)

# CSV'den veriyi güncelle
def update_data():
    global data_storage
    try:
        with open('lora_data.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            data_storage = list(reader)
            socketio.emit('update', data_storage)  # Gerçek zamanlı güncelleme
    except FileNotFoundError:
        print("CSV dosyası bulunamadı!")

if __name__ == '__main__':
    socketio.run(app, debug=True)
