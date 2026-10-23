import os
import requests

# Configuration
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


# Perspective API client
def moderate_text(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
        "key": PERSPECTIVE_API_KEY,
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
