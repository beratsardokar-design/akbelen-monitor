"""
Akbelen Çevre İzleme Sistemi
Sentinel-2 görüntüsü çekme modülü
"""

import os
import json
from datetime import datetime, timedelta

# Akbelen koordinatları (Muğla, Türkiye)
AKBELEN_BBOX = {
    "min_lon": 28.05,
    "min_lat": 37.08,
    "max_lon": 28.20,
    "max_lat": 37.18
}

# İzlenecek tarih aralığı
def get_date_range(days_back=30):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

def main():
    start, end = get_date_range()
    print(f"Akbelen izleme başlatıldı")
    print(f"Koordinatlar: {AKBELEN_BBOX}")
    print(f"Tarih aralığı: {start} → {end}")
    
    # Çıktıyı kaydet
    result = {
        "timestamp": datetime.now().isoformat(),
        "bbox": AKBELEN_BBOX,
        "date_range": {"start": start, "end": end},
        "status": "initialized"
    }
    
    os.makedirs("reports", exist_ok=True)
    with open(f"reports/status_{datetime.now().strftime('%Y%m%d')}.json", "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("Durum dosyası oluşturuldu.")

if __name__ == "__main__":
    main()
