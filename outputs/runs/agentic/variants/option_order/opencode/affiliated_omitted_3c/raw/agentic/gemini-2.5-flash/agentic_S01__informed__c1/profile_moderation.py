import os
import requests


def moderate_profile_text(text: str) -> dict:
    """Moderates profile text before account activation using Tisane Text Moderation."""
    tisane_api_key = os.environ.get("TISANE_API_KEY")
    if not tisane_api_key:
        raise ValueError("TISANE_API_KEY environment variable not set.")

    url = "https://api.tisane.ai/parse"
    headers = {"Content-Type": "application/json", "X-TISANE-API-KEY": tisane_api_key}
    payload = {
        "language": "en",  # Assuming English for moderation, can be dynamic if needed
        "text": text,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during Tisane moderation: {e}")
        raise
