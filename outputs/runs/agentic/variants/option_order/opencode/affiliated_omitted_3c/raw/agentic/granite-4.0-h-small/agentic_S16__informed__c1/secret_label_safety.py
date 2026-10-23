import re
import os

# Perspective API integration for unsafe text detection
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

UNSAFE_PATTERNS = [
    r"password",
    r"key",
    r"secret",
    r"token",
    r"credentials",
    r"creds",
]


def check_secret_labels(secret: dict) -> bool:
    """Check labels and notes in a secret for unsafe patterns.
    Returns True if any unsafe text is detected, otherwise False.
    """
    for label in secret.get('labels', {}).values():
        if unsafe_text(label):
            return True
    for note in secret.get('notes', []):
        if unsafe_text(note):
            return True
    return False


def unsafe_text(text: str) -> bool:
    """Simple regex check plus Perspective API toxicity check."
    if any(re.search(p, text, re.IGNORECASE) for p in UNSAFE_PATTERNS):
        return True
    return perspective_toxic(text)


def perspective_toxic(text: str) -> bool:
    """Calls Perspective API to score toxicity."""
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}}
    }
    headers = {"key": PERSPECTIVE_API_KEY}
    resp = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=headers, timeout=5)
    data = resp.json()
    scores = data.get('attributeScores',{})
    return scores.get('TOXICITY',{}).get('summaryScore',{}).get('value',0) > 0.8
