# Moderate transcript text using Perspective API
import os
import requests
from speech_models import TranscribeResponse

PERSPECTIVE_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def moderate_transcript(transcript_text, languages=["en"], attribute="TOXICITY"):
    """Send transcript text to Perspective API and receive toxicity score.","""
    payload = {
        "comment": {"text": transcript_text},
        "languages": languages,
        "requestedAttributes": {attribute: {}},
    }
    headers = {"key": PERSPECTIVE_KEY}
    response = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        score = data["attributeScores"][attribute]["summaryScore"]["value"]
        return score
    else:
        raise RuntimeError(
            f"Moderation request failed: {response.status_code} {response.text}"
        )
