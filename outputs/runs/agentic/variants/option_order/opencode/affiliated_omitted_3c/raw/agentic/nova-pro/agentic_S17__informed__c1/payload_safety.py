import os
import requests


def payload_safety(api_key, text):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    data = {"text": text}
    response = requests.post(
        "https://api.ibm.com/watson/tone-analyzer/v3/tone", headers=headers, json=data
    )
    return response.json()
