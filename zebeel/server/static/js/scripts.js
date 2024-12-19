function loadData(binsUrl, trucksUrl) {
    const map = L.map('map').setView([41.015137, 28.979530], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);

    // Bins verilerini yükle
    fetch(binsUrl)
        .then(response => response.json())
        .then(data => {
            data.forEach(bin => {
                L.marker([parseFloat(bin.Lat), parseFloat(bin.Lon)])
                    .bindPopup(`Durum: ${bin.Status} <br> Mesafe: ${bin.Distance}cm`)
                    .addTo(map);
            });
        });

    // Trucks verilerini yükle
    fetch(trucksUrl)
        .then(response => response.json())
        .then(data => {
            data.forEach(truck => {
                L.circleMarker([parseFloat(truck.Lat), parseFloat(truck.Lon)], { color: 'blue' })
                    .bindPopup(`Kamyon ID: ${truck.ID}`)
                    .addTo(map);
            });
        });
}
