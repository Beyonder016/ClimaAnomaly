# epic_fetcher.py

import requests
import os
from datetime import datetime

# Base URL for NASA EPIC API
EPIC_API_BASE = "https://epic.gsfc.nasa.gov/api/natural/date/"
EPIC_IMAGE_BASE = "https://epic.gsfc.nasa.gov/archive/natural"

# Directory to store images
epic_dir = "data_cache/epic_images"
os.makedirs(epic_dir, exist_ok=True)

def fetch_epic_thumbnails(date_str):
    """
    Fetch EPIC satellite thumbnails for a given date (YYYY-MM-DD).

    Parameters:
        date_str (str): Date in 'YYYY-MM-DD' format

    Returns:
        List of dicts with 'image', 'caption', 'url'
    """
    url = f"{EPIC_API_BASE}{date_str}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"[ERROR] No EPIC data available for {date_str}")
        return []

    data = response.json()
    results = []

    for item in data:
        image_name = item['image']
        caption = item['caption']
        dt = datetime.strptime(item['date'], "%Y-%m-%d %H:%M:%S")
        image_url = f"{EPIC_IMAGE_BASE}/{dt.strftime('%Y/%m/%d')}/jpg/{image_name}.jpg"

        results.append({
            "image": image_name,
            "caption": caption,
            "url": image_url,
            "datetime": dt.strftime("%Y-%m-%d %H:%M:%S")
        })

    return results

# Example usage
if __name__ == "__main__":
    images = fetch_epic_thumbnails("2023-07-10")
    for img in images[:2]:  # Show only first 2 entries
        print(f"{img['datetime']}: {img['url']}")
