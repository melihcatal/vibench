import os
import requests

TISANE_API_KEY = os.getenv("TISANE_API_KEY")


def moderate_batch(messages):
    url = "https://api.tisane.ai/v1/moderation"
    headers = {"Authorization": f"Bearer {TISANE_API_KEY}"}
    data = {"messages": messages}
    response = requests.post(url, json=data, headers=headers)
    return response.json()
