"""
Akbelen Çevre İzleme Sistemi
Sentinel-2 NDVI analizi - Copernicus Data Space
"""

import os
import json
import requests
from datetime import datetime, timedelta

# Akbelen koordinatları
BBOX = [28.05, 37.08, 28.20, 37.18]
INSTANCE_ID = os.environ.get("COPERNICUS_INSTANCE_ID", "")

def get_token():
    """Copernicus erişim token'ı al"""
    url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    data = {
        "client_id": "cdse-public",
        "username": os.environ.get("COPERNICUS_EMAIL", ""),
        "password": os.environ.get("COPERNICUS_PASSWORD", ""),
        "grant_type": "password"
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def fetch_ndvi_stats():
    """Akbelen için NDVI istatistikleri çek"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    url = f"https://sh.dataspace.copernicus.eu/ogc/wms/{INSTANCE_ID}"
    params = {
        "SERVICE": "WMS",
        "REQUEST": "GetMap",
        "LAYERS": "VEGETATION_INDEX",
        "BBOX": f"{BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]}",
        "WIDTH": "512",
        "HEIGHT": "512",
        "FORMAT": "image/png",
        "TIME": f"{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}",
        "MAXCC": "20"
    }
    
    response = requests.get(url, params=params)
    return response.status_code == 200

def main():
    print(f"Akbelen NDVI izleme başladı: {datetime.now().isoformat()}")
    
    success = fetch_ndvi_stats()
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "bbox": BBOX,
        "ndvi_fetch_success": success,
        "status": "success" if success else "error"
    }
    
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/akbelen_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Rapor kaydedildi: {filename}")
    print(f"NDVI çekme: {'Başarılı' if success else 'Hata'}")

if __name__ == "__main__":
    main()
