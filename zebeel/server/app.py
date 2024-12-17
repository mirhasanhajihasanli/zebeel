from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Veri dosyasının yolu
CSV_FILE = "data/lora_data.csv"

# Ana Sayfa (Admin Ekranı)
@app.route("/")
def index():
    return render_template("admin.html")

# Çöp Kutuları Verilerini JSON Olarak Gönder
@app.route("/get_bins")
def get_bins():
    try:
        df = pd.read_csv(CSV_FILE)
        bins = df.to_dict(orient="records")  # CSV'yi sözlük listesine çevir
        return jsonify(bins)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
