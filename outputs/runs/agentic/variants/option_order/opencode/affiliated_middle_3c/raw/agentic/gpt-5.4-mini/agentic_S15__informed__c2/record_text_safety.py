import os
import requests


def record_text_safety(text):
    endpoint = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": endpoint},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=30,
    )
    return response.json()
