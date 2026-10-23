import os

import requests


def moderate_transcript(text):
    endpoint = os.environ["PERSPECTIVE_API_ENDPOINT"]
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        endpoint,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=30,
    )
    return response.json()
