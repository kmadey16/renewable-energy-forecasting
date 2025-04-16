import requests
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("NREL_API_KEY")


def fetch_solar_data(lat=29.7604, lon=-95.3698):
    url = "https://developer.nrel.gov/api/solar/solar_resource/v1.json"
    params = {
        "api_key": API_KEY,
        "lat": lat,
        "lon": lon
    }

    response = requests.get(url, params=params)
    data = response.json()

# Save to data/raw with timestamp
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"data/raw/solar_nrel_{ts}.json"

    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved solar data to {out_path}")

if __name__ == "__main__":
    fetch_solar_data()