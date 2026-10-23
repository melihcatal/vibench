import json
import requests


def moderate_vendor_notes(text, api_key):
    # Simple example using placeholder moderation API endpoint
    url = "https://api.example.com/moderate"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"text": text}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result.get("is_safe", False), result.get("flagged_reason", "")
    else:
        raise Exception("Moderation request failed")
