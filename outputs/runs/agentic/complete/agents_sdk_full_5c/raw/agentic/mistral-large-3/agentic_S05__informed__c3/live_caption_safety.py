import os
import requests
from speech_models import TranscriptEvent

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_unsafe_content(event: TranscriptEvent) -> dict:
    if not event.is_final:
        return {}
    params = {
        "key": PERSPECTIVE_API_KEY,
    }
    data = {
        "comment": {"text": event.text},
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=data)
    return response.json().get("attributeScores", {})