import os
import requests

# [LATER-STEP] metric_annotation_safety.py


def metric_annotation_safety(text):
    url = "https://api.perspectiveapi.com/v1/comment"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('PERSPECTIVE_API_KEY')}",
    }
    data = {"comment": {"text": text}}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
