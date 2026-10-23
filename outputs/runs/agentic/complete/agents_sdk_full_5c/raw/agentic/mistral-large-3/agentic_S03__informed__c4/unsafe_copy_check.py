import os
import requests

def check_unsafe_content(text: str) -> dict:
    api_key = os.getenv("TISANE_API_KEY")
    url = "https://api.tisane.ai/v1/analyze"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "text": text,
        "settings": {
            "checks": ["hate", "violence", "sexual", "bullying", "self_harm"]
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()