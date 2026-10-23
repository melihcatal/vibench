import os

import requests


PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_prompt(text):
    response = requests.post(
        f"{PERSPECTIVE_URL}?key={os.getenv('PERSPECTIVE_API_KEY')}",
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
