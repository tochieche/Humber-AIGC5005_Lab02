import json 
from collections import Counter, defaultdict, deque, namedtuple
from pathlib import Path
import sys
import requests

SOURCE_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=43.65&longitude=-79.38"
    "&hourly=temperature_2m,precipitation"
    "&past_days=7&forecast_days=0"
    "&timezone=America%2FToronto"
)
OUTPUT = Path("summary.json")

# namedtuple to cleanly structure valid weather records
HourlyRecord = namedtuple("HourlyRecord", ["timestamp", "temperature", "precipitation"])


def fetch_records(url):
    # Downloads hourly weather data from the wather API URL as object
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    payload = response.json()

    # process and validate the timestamps, temperatures, and precipitation values into HourlyRecord objects.
    hourly = payload.get("hourly", {})
    timestamps = hourly.get("time", [])
    temperatures = hourly.get("temperature_2m", [])
    precipitations = hourly.get("precipitation", [])

    records = []
    for ts, temp, precip in zip(timestamps, temperatures, precipitations):
        # handles missing or malformed values without crashing or misrepresenting
        if ts is None or temp is None or precip is None:
            continue
        try:
            valid_temp = float(temp)
            valid_precip = float(precip)
            records.append(
                HourlyRecord(
                    timestamp=str(ts),
                    temperature=valid_temp,
                    precipitation=valid_precip,
                )
            )
        # raises an exception on network or HTTP errors.
        except (ValueError, TypeError):
            continue

    return records
