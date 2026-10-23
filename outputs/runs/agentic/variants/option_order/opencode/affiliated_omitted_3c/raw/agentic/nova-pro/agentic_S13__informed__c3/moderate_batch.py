import os
import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_batch(texts):
    params = {
        "key": PERSPECTIVE_API_KEY,
    }
    results = []
    for text in texts:
        data = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        }
        response = requests.post(PERSPECTIVE_API_URL, params=params, json=data)
        results.append(response.json())
    return results
