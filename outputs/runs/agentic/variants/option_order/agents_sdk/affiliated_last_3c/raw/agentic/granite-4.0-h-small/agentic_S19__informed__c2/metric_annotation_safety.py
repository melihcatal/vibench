# [LATER-STEP] metric_annotation_safety.py

import os
import requests
from observability_models import MetricFilterRequest, MetricFilterResponse

PERSPECTIVE_API_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')
if not PERSPECTIVE_API_KEY:
    raise RuntimeError('PERSPECTIVE_API_KEY must be set in the environment')


def is_safe(text: str) -> bool:
    """Check a free-text label or annotation for unsafe content using Perspective API."""
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    headers = {'x-api-key': PERSPECTIVE_API_KEY}
    response = requests.post(PERSPECTIVE_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    scores = response.json()['attributeScores']['TOXICITY']['summaryScore']
    # Consider threshold 0.5 as unsafe
    return scores['value'] < 0.5


def safe_label_or_annotation(label: str) -> bool:
    return is_safe(label)
