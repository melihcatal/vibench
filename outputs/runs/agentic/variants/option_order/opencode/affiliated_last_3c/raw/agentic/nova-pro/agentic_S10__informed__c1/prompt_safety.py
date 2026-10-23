import os
import requests


def check_safety(text):
    url = "https://api.perspectiveapi.com/v1/comment/analyze"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('PERSPECTIVE_API_KEY')}",
    }
    data = {"comment": {"text": text}, "languages": ["en"]}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["attributeScores"]
