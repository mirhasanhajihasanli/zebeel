

document.addEventListener("DOMContentLoaded", function () {
    // Harita oluştur
    var map = L.map('map').setView([41.0, 29.0], 12); // İstanbul merkezli başlangıç

    // OpenStreetMap katmanı ekle
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '© OpenStreetMap'
    }).addTo(map);

    // Veriyi çek ve haritaya ekle
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                var color = item.Status === "Full" ? "red" : item.Status === "Medium" ? "orange" : "green";
                L.circleMarker([item.Lat, item.Lon], {
                    color: color,
                    radius: 10
                }).addTo(map)
                .bindPopup(`<b>Doluluk:</b> ${item.Status}<br><b>Mesafe:</b> ${item.Distance} cm`);
            });
        });
});
