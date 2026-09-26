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


# Aggregate by date groups using a dictionary and computes statistics on classes of weather conditions alognside categories.
def aggregate_by_date(records):
    
    #Group weather records by date using a dictionary
    grouped = defaultdict(list)
    for rec in records:
        date_str = rec.timestamp.split("T")[0]
        grouped[date_str].append(rec)

    # building a dictionary of aggregations per date and returns min, max, and average temperature along with total precipitation per date.
    return {
        date: {
            "min_temp_c": round(min(r.temperature for r in day_recs), 1),
            "max_temp_c": round(max(r.temperature for r in day_recs), 1),
            "avg_temp_c": round(
                sum(r.temperature for r in day_recs) / len(day_recs), 1
            ),
            "total_precip_mm": round(sum(r.precipitation for r in day_recs), 1),
            "readings": len(day_recs),
        }
        for date, day_recs in grouped.items()
    }

# Classify hourly readings into condition categories and count their frequencies using a collection
def classify_weather_conditions(records):
    # frequency of weather condition classifications.
    conditions = []
    for rec in records:
        if rec.precipitation > 0.0:
            conditions.append("Precipitation")
        elif rec.temperature < 0.0:
            conditions.append("Freezing Dry")
        elif rec.temperature < 15.0:
            conditions.append("Cool Dry")
        else:
            conditions.append("Warm Dry")

    # Frequencies on classifications of weather conditions 
    return dict(Counter(conditions))

# Retrieve the last hourly records using a fixed-size to show recent trends.
def recent_readings(records, count=5):
     # deque with maxlen to maintain a the recent records
    recent_queue = deque(maxlen=count)
    for rec in records:
        recent_queue.append(
            {
                "timestamp": rec.timestamp,
                "temperature_c": rec.temperature,
                "precipitation_mm": rec.precipitation,
            }
        )
    return list(recent_queue)
