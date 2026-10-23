import os
import requests


def generate_audio_brief(text, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["AUDIO_BRIEF_API_KEY"]
    response = requests.post("https://api.audiobrief.com/v1/generate", json={"text": text}, headers={"Authorization": f"Bearer {api_key}"})
    response.raise_for_status()
    return response.json()