
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
A short excerpt of summary.json, and what it tells you.

## Data quirks
Each problem you found in the data, and what your program does about it.

## Design choices
Which collection types you used and why each was the right choice.

## Known limitations
Anything that does not work, or that you would improve with more time.