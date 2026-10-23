import os
import requests
from messaging_models import Event

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
perspective_key = os.getenv("PERSPECTIVE_API_KEY")


def check_message_safety(event: Event) -> bool:
    text = str(event.payload)
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    response = requests.post(
        PERSPECTIVE_API_URL, params={"key": perspective_key}, json=payload
    )
    scores = response.json().get("attributeScores", {})
    toxicity = scores.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0)
    return toxicity < 0.5
