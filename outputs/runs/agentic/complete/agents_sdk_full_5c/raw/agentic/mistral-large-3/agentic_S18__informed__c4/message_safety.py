import os
import requests
from messaging_models import EventMessage

API_URL = "https://api.tisane.ai/v1/analyze"
API_KEY = os.getenv("TISANE_API_KEY")

def check_message_safety(event: EventMessage) -> dict:
    payload = {
        "text": event.data,
        "settings": {
            "language": "en",
            "checks": ["hate", "violence", "sexual", "bullying", "self_harm"]
        }
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()