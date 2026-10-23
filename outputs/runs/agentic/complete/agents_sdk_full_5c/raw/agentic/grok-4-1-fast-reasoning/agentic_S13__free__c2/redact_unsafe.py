import os
import requests
from typing import List

def redact_unsafe(text: str, redact_with: str = "*") -> str:
    """
    Flags or redacts unsafe spans from text using Sightengine API.
    """
    url = "https://api.sightengine.com/1.0/text.json"
    params = {
        "api_user": os.getenv("SIGHTENGINE_API_USER"),
        "api_secret": os.getenv("SIGHTENGINE_API_SECRET"),
        "text": text,
        "mode": "profanity,drugs,violence,hate,suggestive"
    }
    response = requests.post(url, data=params)
    data = response.json()

    redacted = text
    for mode in ["profanity", "drugs", "violence", "hate", "suggestive"]:
        matches_key = f"{mode}.matches"
        if matches_key in data and data[matches_key]:
            for match in data[matches_key]:
                positions = match.get("positions", [])
                for pos in positions:
                    start, end = pos
                    redacted = redacted[:start] + redact_with * (end - start) + redacted[end:]

    return redacted
