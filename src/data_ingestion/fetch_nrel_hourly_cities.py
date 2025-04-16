import requests
import time
import os
import json
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("NREL_API_KEY")
EMAIL = "kmadey16@gmail.com"

BASE_URL = "https://developer.nrel.gov/api/nsrdb/v2/solar/nsrdb-GOES-aggregated-v4-0-0-download.json"

# Manually mapped nearby location IDs for each city
CITIES = {
    "houston_tx": "722997",
    "phoenix_az": "747187",
    "seattle_wa": "727930",
    "denver_co": "725650",
    "miami_fl": "722020"
}

ATTRIBUTES = (
    "dhi,ghi,dni,wind_speed,air_temperature,relative_humidity,"
    "clearsky_dhi,clearsky_dni,clearsky_ghi,total_precipitable_water,"
    "wind_direction,surface_albedo,surface_pressure,solar_zenith_angle,dew_point"
)

def get_response_json_and_handle_errors(response: requests.Response) -> dict:
    if response.status_code != 200:
        print(f"❌ HTTP {response.status_code}: {response.reason}")
        print(response.text)
        return None

    try:
        response_json = response.json()
    except Exception:
        print(f"❌ Failed to parse JSON:\n{response.text}")
        return None

    if response_json.get("errors"):
        print("❌ API returned errors:")
        for e in response_json["errors"]:
            print(f"  - {e}")
        return None

    return response_json

def main():
    headers = {
        "x-api-key": API_KEY
    }

    for year in ["2022", "2023"]:
        for city, location_id in CITIES.items():
            print(f"📡 Requesting {year} data for {city} (ID: {location_id})")

            payload = {
                "attributes": ATTRIBUTES,
                "interval": "60",
                "include_leap_day": "true",
                "to_utc": "false",
                "api_key": API_KEY,
                "email": EMAIL,
                "names": year,
                "location_ids": location_id
            }

            try:
                response = requests.post(BASE_URL, data=payload, headers=headers)
                data = get_response_json_and_handle_errors(response)

                if not data:
                    continue

                download_url = data["outputs"]["downloadUrl"]
                message = data["outputs"]["message"]

                print(f"✅ {city} {year}: {message}")
                print(f"🔗 Download: {download_url}")

                # Download the CSV
                csv_response = requests.get(download_url)
                os.makedirs("data/raw", exist_ok=True)
                out_path = f"data/raw/{city}_{year}_nrel_goes.csv"

                with open(out_path, "wb") as f:
                    f.write(csv_response.content)

                print(f"📁 Saved to: {out_path}\n")

                # Wait to avoid rate limiting
                time.sleep(5)

            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                continue

if __name__ == "__main__":
    main()

