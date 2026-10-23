import os
import requests


def check_safety(text):
    url = "https://api.perspectiveapi.com/v1/comment"
    headers = {
        "Content-Type": "application/json",
        "Key": os.getenv("PERSPECTIVE_API_KEY"),
    }
    data = {"comment": {"text": text}, "languages": ["en"]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
