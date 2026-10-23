import os
import requests
from observability_client import get_log_client, put_log

# Perspective API (Google) content safety check
# Requires environment variable PERSPECTIVE_API_KEY

PERSPECTIVE_API_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
API_KEY = os.getenv('PERSPECTIVE_API_KEY')
if not API_KEY:
    raise RuntimeError('Set PERSPECTIVE_API_KEY environment variable')


def is_log_text_safe(text: str) -> bool:
    """Check whether a log message contains unsafe content using Perspective API.

    :param text: Raw log message string.
    :return: True if safe, False if unsafe.
    """
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'THREAT': {}, 'INSULT': {}, 'PROFANITY': {}}
    }
    headers = {'x-api-key': API_KEY}
    resp = requests.post(PERSPECTIVE_API_URL, json=payload, headers=headers)
    resp.raise_for_status()
    result = resp.json()['attributeScores']
    # Consider unsafe if TOXICITY or SEVERE_TOXICITY scores exceed 0.5
    toxic_score = result.get('TOXICITY', {}).get('summaryScore', {}).get('value', 0)
    severe_score = result.get('SEVERE_TOXICITY', {}).get('summaryScore', {}).get('value', 0)
    return toxic_score < 0.5 and severe_score < 0.5
