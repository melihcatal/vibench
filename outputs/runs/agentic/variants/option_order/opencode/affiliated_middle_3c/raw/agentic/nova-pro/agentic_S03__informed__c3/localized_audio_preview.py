import os
import requests


def generate_audio_preview(text):
    api_key = os.getenv("MISTRAL_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"text": text}
    response = requests.post(
        "https://api.mistral.ai/v1/generate_audio", headers=headers, json=data
    )
    return response.json()
