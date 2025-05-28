#!/usr/bin/env python3
import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from local/.env
load_dotenv(Path(__file__).parent.parent / "local" / ".env")

# Get API key
api_key = os.getenv("CBORG_API_KEY")
if not api_key:
    print("Error: CBORG_API_KEY not found in local/.env")
    exit(1)

# Make the request
response = requests.get(
    "https://api.cborg.lbl.gov/key/info", headers={"Authorization": f"Bearer {api_key}"}
)

# Print the result (pretty-printed JSON)
if response.status_code == 200:
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)
