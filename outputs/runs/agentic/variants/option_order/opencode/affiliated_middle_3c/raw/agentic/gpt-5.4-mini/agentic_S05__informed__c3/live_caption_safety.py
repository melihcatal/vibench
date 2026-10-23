import os

import requests

from speech_models import normalize_text


def check_caption_safety(text: str) -> dict:
    payload = {"comment": {"text": normalize_text(text)}, "languages": ["en"]}
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": os.environ.get("PERSPECTIVE_API_KEY", "")},
        json={**payload, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
