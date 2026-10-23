import os
import requests


def check_safety(text):
    url = "https://api.perspectiveapi.com/v1/models/toxicity/classify"
    headers = {
        "Content-Type": "application/json",
        "Key": os.getenv("PERSPECTIVE_API_KEY"),
    }
    data = {"comment": {"text": text}, "languages": ["en"]}
    response = requests.post(url, json=data, headers=headers)
    return response.json()
