import os
import requests


def embed_translated_segment(text):
    api_key = os.getenv("MISTRAL_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"text": text}
    response = requests.post(
        "https://api.mistral.ai/v1/embed", headers=headers, json=data
    )
    return response.json()
