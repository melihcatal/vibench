import os
from google.cloud import translate_v2 as translate

# Local helpers
from translation_client import get_translation_client
from translation_models import validate_text

def check_unsafe_content(translated_text: str) -> list[str]:
    """Runs a basic safety check on translated text using Perspective API.

    Returns a list of detected unsafe categories (e.g., 'TOXICITY', 'THREAT').
    """
    client = get_translation_client()
    # Perspective API is a REST endpoint; we call it directly
    PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')
    if not PERSPECTIVE_API_KEY:
        raise RuntimeError('Set PERSPECTIVE_API_KEY environment variable')
    import json, requests
    payload = {
        "comment": {
            "text": translated_text
        },
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "THREAT": {},
            "INSULT": {},
            "PROFANITY": {}
        }
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": PERSPECTIVE_API_KEY
    }
    resp = requests.post(PERSPECTIVE_API_URL, data=json.dumps(payload), headers=headers)
    resp.raise_for_status()
    attributes = resp.json()['attributeScores']
    issues = []
    for attr, scores in attributes.items():
        if scores.get('summaryScore', {}).get('value', 0) > 0.8:
            issues.append(attr)
    return issues

if __name__ == "__main__":
    txt = "You are a fool."
    print(check_unsafe_copy_check(txt))