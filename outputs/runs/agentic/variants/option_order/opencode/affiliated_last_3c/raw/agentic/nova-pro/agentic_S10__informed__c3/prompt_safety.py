import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def check_safety(text):
    headers = {"Content-Type": "application/json"}
    data = {"comment": {"text": text}, "languages": ["en"]}
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + PERSPECTIVE_API_KEY,
        headers=headers,
        json=data,
    )
    return response.json()
