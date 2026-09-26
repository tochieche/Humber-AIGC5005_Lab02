
# Weather App Builder
This program downloads a week of hourly temperature and rain data for Toronto from an open API and summarizes it into daily stats and weather patterns. It's useful because looking through hundreds of raw weather numbers is annoying, so this automatically breaks down the highs, lows, averages, and rainfall for you.

## Data source
The data comes from the [Open-Meteo Weather API](https://api.open-meteo.com/v1/forecast?latitude=43.65&longitude=-79.38&hourly=temperature_2m,precipitation&past_days=7&forecast_days=0&timezone=America/Toronto). One record represents one hour of weather data (containing a timestamp, temperature in °C, and precipitation in mm), and the API returns around 168 records for a full 7-day period.

## Setup
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt

## Run
python records.py

## Example output
The retrieved output sample json is as follows:
{
  "source_url": "[https://api.open-meteo.com/v1/forecast]",
  "records_processed": 168,
  "hottest_day": "2026-09-21",
  "hottest_day_max_temp_c": 22.4,
  "daily_breakdown": {
    "2026-09-21": {
      "min_temp_c": 13.0,
      "max_temp_c": 22.4,
      "avg_temp_c": 17.8,
      "total_precip_mm": 1.2,
      "readings": 24
    }
  }
}

## Data quirks
The API doesn't return a list of neat JSON dictionaries; instead, it gives separate arrays for timestamps, temperatures, and precipitation. My code combines them into a single record.

Sometimes the API can have missing or null values or values that aren't numbers. My program checks for this and uses a try/except block to skip any corrupted readings instead of crashing or accidentally treating missing data as 0°C.


## Design choices
I used namedtuple to store each hourly reading so I could access fields like rec.temperature instead of using array indexes.

I used defaultdict for grouping hourly records by date. It saves time by automatically creating a new list for a date key if it doesn't exist yet.

I used tally to determine how many hours fell under categories like Cool Dry or Precipitation without having to write extra dictionary loop code.

I used deque with maxlen=5 so I could easily keep a rolling buffer of only the 5 most recent weather readings without manually trimming a list.


## Known limitations
The API URL is currently hardcoded for Toronto and 7 past days. If I had more time, I'd let the user type in custom city coordinates or select a different date range using command-line arguments.

The temperature categories use hardcoded numbers like 15°C, which might not make sense if you ran this for a location in a completely different season or climate zone.