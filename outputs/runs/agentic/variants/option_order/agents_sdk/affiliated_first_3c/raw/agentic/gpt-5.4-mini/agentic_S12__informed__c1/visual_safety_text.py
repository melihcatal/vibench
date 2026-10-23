import requests


PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def visual_safety_text(text: str, api_key: str) -> dict:
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    response = requests.post(f"{PERSPECTIVE_URL}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
