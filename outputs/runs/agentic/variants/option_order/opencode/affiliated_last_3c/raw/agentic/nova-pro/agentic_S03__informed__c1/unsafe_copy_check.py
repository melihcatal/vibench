import os
import requests


def unsafe_copy_check(text):
    api_key = os.getenv("TISANE_API_KEY")
    url = "https://api.tisane.ai/v1/check"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"text": text}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
