import os

TISANE_API_KEY = os.getenv("TISANE_API_KEY")

import requests


def moderate_text(text):
    url = "https://api.tisane.ai/v1/moderate"
    headers = {"Authorization": f"Bearer {TISANE_API_KEY}"}
    data = {"text": text}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
