# ZebeeL | Akıllı Atık Yönetim Sistemi

ZebeeL, sensör tabanlı **Akıllı Atık Yönetim Sistemi** geliştirerek atık toplama süreçlerini optimize eder ve verimliliği artırır. Bu sistem, atık kutularının doluluk oranını izlemek, rota optimizasyonu sağlamak ve atık toplama operasyonlarını daha verimli hale getirmek için **IoT sensörleri**, **bulut tabanlı veri işleme** ve **mobil/web uygulamaları** kullanır.

---

## 📊 Proje Amaçları
- Atık toplama işleminde **zamandan ve maliyetten tasarruf** sağlamak.
- Trafik ve doluluk seviyelerine göre **rota optimizasyonu** yapmak.
- **Gerçek zamanlı izleme** ile atık kutularının doluluk oranlarını takip etmek.
- Karbon emisyonunu azaltarak çevresel etkileri en aza indirmek.

---

## 🛠️ Teknolojiler ve Araçlar
Bu projede kullanılan temel teknolojiler ve bileşenler:

### Donanım:
- **Raspberry Pi 4 (8GB)**
- **HC-SR04 Ultrasonik Sensör** (Doluluk seviyesi algılama)
- **RA-02 LoRa Modülü** (Kablosuz haberleşme)
- **Quectel L86-M33 GNSS** (Konum belirleme)
- **LED Göstergeler** (Doluluk durumu bildirimi)
- **1/4W 330Ω Dirençler** (Gerilim düzenlemesi)

### Yazılım:
- **Raspberry Pi OS (64-bit)**
- **Python** (Veri işleme, sensör kontrolü)
- **Django + Django REST Framework** (Backend API)
- **React.js** (Web Arayüzü)
- **MQTT Protokolü** (IoT sensör iletişimi)
- **MySQL/MongoDB** (Veritabanı)
- **AWS/Azure** (Bulut barındırma)

---

## 🔄 Sistemin Bileşenleri

1. **Atık Kutuları İçin Sensörler:**
   - HC-SR04 Ultrasonik sensörler, atık kutularının doluluk seviyelerini algılar.
   
2. **IoT Haberleşme Ağı:**
   - LoRa modülü kullanılarak veriler uzak mesafelere aktarılır.

3. **Veri İşleme Backend Sistemi:**
   - Django REST API, IoT sensör verilerini toplar ve işler.

4. **Kullanıcı Arayüzleri:**
   - **Yönetici Paneli:** Atık toplama rotalarını optimize eder ve verileri analiz eder.
   - **Mobil/Web Arayüz:** Çalışanlar için atık toplama operasyonlarını takip eder.

5. **Rota Optimizasyonu:**
   - Gerçek zamanlı trafik ve doluluk verilerini analiz ederek en iyi toplama rotasını hesaplar.

---

## 🛢️ Kurulum ve Çalıştırma

### 1. Donanım Kurulumu
- HC-SR04 sensörü Raspberry Pi'ye bağlayın (ECHO pinine direnç ekleyin).
- LoRa modülünü GNSS anteniyle bağlantı kurarak Raspberry Pi'ye ekleyin.

### 2. Yazılım Kurulumu
1. Raspberry Pi'de Python için gerekli kütüphaneleri kurun:
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip
   pip3 install django djangorestframework paho-mqtt
   ```
2. Django backend'i çalıştırın:
   ```bash
   python3 manage.py runserver
   ```
3. React.js arayüzü için:
   ```bash
   npm install
   npm start
   ```

### 3. API Testi
- Backend API'ye istek yapmak için `Postman` veya benzeri bir araç kullanın.

### 4. IoT Bağlantısı
- Sensörlerden MQTT ile veri aktarımını test edin.

---

## 🌐 Lisans
Bu proje **Apache 2.0** lisansı altında yayınlanmıştır. Daha fazla bilgi için [Lisans Dosyasına](LICENSE) göz atabilirsiniz.

---

## 🔗 Katkıda Bulunma
Projeye katkıda bulunmak isterseniz:
1. **Fork** yapın.
2. Yeni bir **branch** oluşturun.
3. Değişiklikleri yapın ve bir **Pull Request** gönderin.

Her türlü geri bildirime ve katkıya açığız! İyi kodlamalar 💪

---

## 👥 Ekip
- **Proje Yöneticisi:** Mirhasan Haji Hasanli
---
