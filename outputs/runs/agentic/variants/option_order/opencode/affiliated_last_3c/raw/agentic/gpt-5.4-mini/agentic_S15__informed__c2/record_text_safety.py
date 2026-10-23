import os

import requests


def check_safety(text):
    resp = requests.post(
        "https://api.perspectiveapi.com/v1/comments:analyze",
        params={"key": os.getenv("PERSPECTIVE_API_KEY")},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    return resp.json()
