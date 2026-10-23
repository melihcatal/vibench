import os
import requests

# Environment variable for the moderation endpoint
PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

if not PERSPECTIVE_API_KEY:
    raise RuntimeError('PERSPECTIVE_API_KEY environment variable not set')

MODERATION_ENDPOINT = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

HEADER = {
    'Content-Type': 'application/json',
    'key': PERSPECTIVE_API_KEY,
}

def check_toxicity(text: str) -> dict:
    """Calls Perspective API to assess toxicity.

    Returns the raw moderation JSON payload."
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(MODERATION_ENDPOINT, headers=HEADER, json=payload)
    response.raise_for_status()
    return response.json()


def is_unsafe(text: str, threshold: float = 0.8) -> bool:
    """Returns True if the text exceeds the toxicity threshold."""
    moderation = check_toxicity(text)
    score = moderation['attributeScores']['TOXICITY']['summaryScore']['value']
    return score >= threshold
