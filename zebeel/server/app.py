from flask import Flask, render_template, jsonify
import csv

app = Flask(__name__)

# CSV dosya yolları
BINS_FILE = 'data/bins.csv'
TRUCKS_FILE = 'data/trucks.csv'

# CSV dosyasını okuma fonksiyonu
def read_csv(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/manager')
def manager():
    return render_template('manager.html')

@app.route('/collector')
def collector():
    return render_template('collector.html')

# API uçları
@app.route('/api/bins')
def get_bins():
    bins = read_csv(BINS_FILE)
    return jsonify(bins)

@app.route('/api/trucks')
def get_trucks():
    trucks = read_csv(TRUCKS_FILE)
    return jsonify(trucks)

if __name__ == "__main__":
    app.run(debug=True)
