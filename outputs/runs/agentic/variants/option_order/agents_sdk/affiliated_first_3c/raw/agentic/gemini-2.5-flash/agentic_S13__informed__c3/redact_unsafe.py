import os
import requests

def redact_unsafe(text: str) -> dict:
    """Flags or redacts unsafe spans from text using Tisane Text Moderation."""
    api_key = os.environ.get("TISANE_API_KEY")
    api_url = "https://api.tisane.ai/parse"

    if not api_key:
        raise ValueError("TISANE_API_KEY environment variable must be set.")

    headers = {
        "X-TISANE-API-KEY": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "language": "en",
        "text": text,
        "settings": {
            "detectToxicity": True,
            "detectProfanity": True,
            "detectHateSpeech": True
        }
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error redacting unsafe content with Tisane: {e}")
        raise
