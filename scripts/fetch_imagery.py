import os
import json
import requests
from datetime import datetime, timedelta

# Akbelen koordinatları - DÜZELTİLDİ
BBOX = [27.83, 37.15, 27.90, 37.20]
INSTANCE_ID = os.environ.get("COPERNICUS_INSTANCE_ID", "")

def fetch_ndvi_image(date_str):
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
    
    image_data = fetch_ndvi_image(time_range)
    
    if image_data:
        img_filename = f"reports/ndvi_{date_str}.png"
        with open(img_filename, "wb") as f:
            f.write(image_data)
        image_saved = True
    else:
        image_saved = False
    
    result = {
        "timestamp": today.isoformat(),
        "date": date_str,
        "bbox": {"min_lon": BBOX[0], "min_lat": BBOX[1], "max_lon": BBOX[2], "max_lat": BBOX[3]},
        "image_saved": image_saved,
        "status": "success" if image_saved else "no_image"
    }
    
    with open(f"reports/rapor_{date_str}.json", "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
