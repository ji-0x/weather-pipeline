#/!usr/bin/env python3


import os 
import sys
import requests
import json
import logging
from dotenv import load_dotenv
from datetime import datetime



# -----------------------------
# Paths
# -----------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'settings.json')
RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

log_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file_path = os.path.join(LOG_DIR,f'ingest_weather_{log_time}.log')


# -----------------------------
# Logging
# -----------------------------

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# -----------------------------
# Load variables from .env
# -----------------------------


load_dotenv()
api_key = os.getenv("API_KEY")
#print(api_key)

if not api_key:
    sys.exit("ERROR: API_KEY not foiund in .env")


# -----------------------------
# Load API Key and Cities
# -----------------------------

def load_config(path):
    try:
        with open(path, 'r') as f:
            config = json.load(f)
        return config

    except FileNotFoundError:
        logger.error(f"Config file not found: {path}")
        sys.exit(1)

    except json.JSONDecodeError:
        logger.error(f"Config file is not Invalid JSON")
        sys.exit(1)


# -----------------------------
# Fetch weater data from API
# -----------------------------

def fetch_weather(api_key, query):
    url=f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={query}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        logger.error(f"Failed to fetch weather for {query}: {e}")
        return None


# -----------------------------
# Save Raw weather data
# -----------------------------

def save_raw_data(city, data):
    # timestamp in ISO 8601 format
    timestamp = datetime.now().isoformat(timespec='seconds').replace(':', '-')
    safe_city = city.lower().replace(' ', '_')
    filename = f"{safe_city}_weather_{timestamp}.json"
    filepath = os.path.join(RAW_DATA_DIR, filename)

    try: 
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Saved weather data for {city} to {filepath}")
        return True

    except Exception as e:
        logger.error(f"Failed to write file for {city} to {e}")
        return False


def main():

    # Load config.json
    config = load_config(CONFIG_PATH)
    # Get cities
    cities = config.get('cities', {})

    # Ensure dir exists
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
    # Get weather data
    for city, coords in cities.items():
        data = fetch_weather(api_key, coords)
        if data:
            save_raw_data(city,  data)


if __name__ == '__main__':
    main()
