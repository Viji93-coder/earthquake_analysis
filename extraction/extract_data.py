import requests
import pandas as pd
import os
from datetime import datetime
import json

URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

BASE_PATH = "data/raw"

os.makedirs(BASE_PATH, exist_ok=True)

current_year = datetime.now().year

start_year = current_year - 5

all_years = []

for year in range(start_year, current_year + 1):

    print(f"\n{'='*50}")
    print(f"Processing Year: {year}")
    print(f"{'='*50}")

    yearly_records = []

    for month in range(1, 13):
        start_date = f"{year}-{month:02d}-01"

        if year == current_year and month > datetime.now().month:
            break
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
        params = {
            "format": "geojson",
            "starttime": start_date,
            "endtime": end_date,
            "minmagnitude": 3
        }
        print(f"Fetching {start_date} -> {end_date}")
        try:

            response = requests.get(URL,params=params)

            if response.status_code != 200:
                print(f"Failed: {response.status_code}")
                continue

            data = response.json()

            with open("output.txt", "w") as file:
                json.dump(data, file)

            
            records = []

            for feature in data.get("features", []):

                props = feature.get("properties", {})
                geom = feature.get("geometry", {})

                coords = geom.get("coordinates",[None, None, None])

                record = {
                    "id": feature.get("id"),                    
                   "mag": props.get("mag"),
                   "place": props.get("place"),
                    "time": props.get("time"),
                    "updated": props.get("updated"),
                   "felt": props.get("felt"),
                   "cdi": props.get("cdi"),           # Community Internet Intensity
                   "mmi": props.get("mmi"),           # Modified Mercalli Intensity
                   "alert": props.get("alert"), 
                   "status": props.get("status"),
                   "tsunami": props.get("tsunami"),
                   "sig": props.get("sig"),           # Significance score
                   "net": props.get("net"),           # Network ID
                   "code": props.get("code"),      
                   "ids": props.get("ids"),              
                   "sources": props.get("sources"),
                   "types": props.get("types"),
                   "nst": props.get("nst"),            # Number of stations
                   "dmin": props.get("dmin"),          # Min. distance to station
                   "rms": props.get("rms"),            # RMS residuals
                   "gap": props.get("gap"),            # Azimuthal gap
                   "magType": props.get("magType"),
                   "type": props.get("type"),
                  "longitude": coords[0],
                   "latitude": coords[1],
                   "depth_km": coords[2]
                }

                records.append(record)

            yearly_records.extend(records)

        except Exception as e:

            print(f"Error {year}-{month:02d}: {e}")

    yearly_df = pd.DataFrame(yearly_records)
    yearly_file = os.path.join(BASE_PATH, f"earthquake_{year}.csv")
    yearly_df.to_csv(yearly_file, index=False)
    print(f"Year {year} completed : {len(yearly_df)} rows")
    all_years.append(yearly_df)

combined_df = pd.concat(all_years, ignore_index=True)
combined_df.to_csv( "data/raw/earthquake_5years_combined.csv", index=False)
print(f"\nTotal Combined Records: {len(combined_df)}")
print("\nExtraction completed successfully")

