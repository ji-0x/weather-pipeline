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


# -----------------------------
# Load variables from .env
# -----------------------------


load_dotenv()
api_key = os.getenv("API_KEY")
print(api_key)

if not api_key:
    sys.exit("ERROR: API_KEY not foiund in .env")

