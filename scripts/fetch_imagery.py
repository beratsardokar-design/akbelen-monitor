"""
Akbelen Çevre İzleme Sistemi
Sentinel-2 NDVI görüntüsü indirme - Copernicus Data Space
"""

import os
import json
import requests
from datetime import datetime, timedelta

# Akbelen koordinatları
BBOX = [# Akbelen Ormanı ve Maden Sahası Odaklı Koordinatlar
BBOX = [28.17, 37.12, 28.20, 37.15]
INSTANCE_ID = os.environ.get("COPERNICUS_INSTANCE_ID", "")

def fetch_ndvi_image(date_str):
    """Belirli tarih için NDVI görüntüsü indir"""
    url = f"https://sh.dataspace.copernicus.eu/ogc/wms/{INSTANCE_ID}"
    params = {
        "SERVICE": "WMS",
        "VERSION": "1.3.0",
        "REQUEST": "GetMap",
        "LAYERS": "VEGETATION_INDEX",
        "BBOX": f"{BBOX[1]},{BBOX[0]},{BBOX[3]},{BBOX[2]}",
        "WIDTH": "512",
        "HEIGHT": "512",
        "FORMAT": "image/png",
        "CRS": "EPSG:4326",
        "TIME": date_str,
        "MAXCC": "30"
    }
    response = requests.get(url, params=params, timeout=30)
    if response.status_code == 200 and len(response.content) > 1000:
        return response.content
    return None

def main():
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    month_ago = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    time_range = f"{month_ago}/{date_str}"
    
    print(f"Akbelen NDVI izleme: {date_str}")
    
    os.makedirs("reports", exist_ok=True)
    
    # NDVI görüntüsü indir
    image_data = fetch_ndvi_image(time_range)
    
    if image_data:
        img_filename = f"reports/ndvi_{date_str}.png"
        with open(img_filename, "wb") as f:
            f.write(image_data)
        print(f"Görüntü kaydedildi: {img_filename}")
        image_saved = True
    else:
        print("Görüntü indirilemedi")
        image_saved = False
    
    # JSON rapor
    result = {
        "timestamp": today.isoformat(),
        "date": date_str,
        "bbox": {
            "min_lon": BBOX[0],
            "min_lat": BBOX[1],
            "max_lon": BBOX[2],
            "max_lat": BBOX[3]
        },
        "image_saved": image_saved,
        "image_file": f"ndvi_{date_str}.png" if image_saved else None,
        "status": "success" if image_saved else "no_image"
    }
    
    report_file = f"reports/rapor_{date_str}.json"
    with open(report_file, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Rapor: {report_file}")
    print(f"Durum: {'Görüntü alındı' if image_saved else 'Görüntü alınamadı'}")

if __name__ == "__main__":
    main()
