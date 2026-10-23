import os
import requests

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


def summarize_audit_events(events):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    response = requests.post(
        "https://api.mistral.ai/v1/summarize", headers=headers, json=events
    )
    return response.json()
