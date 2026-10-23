import os

TISANE_API_KEY = os.getenv("TISANE_API_KEY")

import requests


def create_client():
    return requests.Session()


def moderate_text(client, text):
    url = "https://api.tisane.ai/v1/moderate"
    headers = {"Authorization": f"Bearer {TISANE_API_KEY}"}
    data = {"text": text}
    response = client.post(url, headers=headers, json=data)
    return response.json()
