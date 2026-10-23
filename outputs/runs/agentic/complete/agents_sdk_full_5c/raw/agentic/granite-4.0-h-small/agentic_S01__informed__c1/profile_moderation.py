import os
import requests

# Concrete provider: Perspective API (Google Jigsaw)
PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')
PERSPECTIVE_ENDPOINT = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'


def moderate_profile_text(text: str, language: str = 'en') -> bool:
    """Moderate profile text using Perspective API.

    Returns True if the comment is acceptable (score < 0.5 for SEVERE_TOXICITY).
    """
    payload = {
        'comment': {'text': text, 'type': 'PLAIN_TEXT'},
        'languages': [language],
        'requestedAttributes': {'SEVERE_TOXICITY': {}}
    }
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': PERSPECTIVE_API_KEY
    }
    resp = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=headers)
    resp.raise_for_status()
    scores = resp.json()['attributeScores']['SEVERE_TOXICITY']
    summary = scores['summaryScore']
    # Consider scores >= 0.5 as moderate/severe
    return summary['value'] < 0.5
