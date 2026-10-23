import os

import requests


def check_ocr_safety(text: str) -> dict:
    key = os.environ.get("PERSPECTIVE_API_KEY", "").strip()
    if not key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={key}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
    }
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
