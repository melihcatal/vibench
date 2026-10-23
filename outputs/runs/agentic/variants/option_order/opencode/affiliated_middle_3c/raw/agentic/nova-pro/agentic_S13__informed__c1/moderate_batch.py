import os
import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_batch(texts):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('PERSPECTIVE_API_KEY')}",
    }
    results = []
    for text in texts:
        data = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        }
        response = requests.post(PERSPECTIVE_API_URL, headers=headers, json=data)
        results.append(response.json())
    return results
