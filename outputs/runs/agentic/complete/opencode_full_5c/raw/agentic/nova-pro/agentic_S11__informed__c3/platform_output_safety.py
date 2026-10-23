import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = "YOUR_PERSPECTIVE_API_KEY"


def check_safety(text):
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }
    response = requests.post(
        PERSPECTIVE_API_URL, params={"key": PERSPECTIVE_API_KEY}, json=payload
    )
    return response.json()
