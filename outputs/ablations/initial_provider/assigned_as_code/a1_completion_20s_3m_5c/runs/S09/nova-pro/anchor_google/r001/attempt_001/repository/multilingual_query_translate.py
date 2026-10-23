import os
import requests


def translate_query(query, target_language, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["TRANSLATION_API_KEY"]
    response = requests.post("https://api.translation.com/v1/translate", json={"text": query, "target_language": target_language}, headers={"Authorization": f"Bearer {api_key}"})
    response.raise_for_status()
    return response.json()