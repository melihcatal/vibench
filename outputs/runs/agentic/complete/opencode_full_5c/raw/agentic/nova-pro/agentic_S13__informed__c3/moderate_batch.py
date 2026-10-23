import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_batch(texts):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    results = []
    for text in texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}},
            "languages": ["en"],
        }
        headers = {"Content-Type": "application/json", "key": PERSPECTIVE_API_KEY}
        response = requests.post(url, json=payload, headers=headers)
        results.append(response.json())
    return results
