import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

serp_api_key = os.getenv("SERP_API_KEY")
params = {
    "engine": "google_shopping",
    "q": "ps5",
    "api_key": serp_api_key,
    "gl": "in",
    "hl": "en",
    "num": 20,
}

response = requests.get("https://serpapi.com/search", params=params)
with open("serpapi_dump.json", "w") as f:
    json.dump(response.json(), f, indent=2)

print("Done")
