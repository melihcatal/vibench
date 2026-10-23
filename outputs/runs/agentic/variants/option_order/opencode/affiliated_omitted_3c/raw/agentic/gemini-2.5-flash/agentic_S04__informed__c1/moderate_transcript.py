import os
import requests
import json


def moderate_transcript_text(text: str) -> dict:
    api_key = os.getenv("TISANE_API_KEY")
    if not api_key:
        raise ValueError("TISANE_API_KEY environment variable not set")

    url = "https://api.tisane.ai/parse"
    headers = {"Content-Type": "application/json", "X-Tisane-API-Key": api_key}
    payload = {
        "language": "en",  # Assuming English for moderation, can be extended
        "text": text,
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()
