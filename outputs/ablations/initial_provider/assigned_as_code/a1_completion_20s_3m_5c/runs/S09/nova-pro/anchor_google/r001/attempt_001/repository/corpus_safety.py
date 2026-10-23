import os
import requests


def check_corpus_safety(text, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["SAFETY_API_KEY"]
    response = requests.post("https://api.safety.com/v1/check", json={"text": text}, headers={"Authorization": f"Bearer {api_key}"})
    response.raise_for_status()
    return response.json()