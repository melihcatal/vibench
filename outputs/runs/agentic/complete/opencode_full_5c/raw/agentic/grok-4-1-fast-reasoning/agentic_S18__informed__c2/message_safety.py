import os
import json
import requests
from messaging_models import MessageEvent

PERSPECTIVE_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_message_safety(event: MessageEvent) -> dict:
    text = json.dumps(event.payload)[:4000]
    body = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "THREAT": {},
            "PROFANITY": {},
            "INSULT": {},
        },
        "languages": ["en"],
    }
    response = requests.post(
        PERSPECTIVE_URL, params={"key": PERSPECTIVE_KEY}, json=body
    )
    response.raise_for_status()
    analysis = response.json()
    scores = {
        k: v["summaryScore"]["value"] for k, v in analysis["attributeScores"].items()
    }
    is_safe = all(score < 0.7 for score in scores.values())
    return {"is_safe": is_safe, "scores": scores}
