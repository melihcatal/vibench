import os
import requests

def check_corpus_safety(text: str, api_key: str) -> bool:
    """Call a content safety API to verify whether the corpus text is safe for embedding.
    Provider: Perspective API (Google) – identifiable by the REST endpoint `perspectiveapi.com` and `PERSPECTIVE_API_KEY` env var.
    Returns True if the toxicity score is below the configured threshold, False otherwise.
    """
    endpoint = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    params = {
        'attributeScores': 'TOXICITY',
        'languages': ['en']
    }
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(endpoint, json=payload, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    scores = data.get('attributeScores', {}).get('TOXICITY', {}).get('summaryScore', {})
    score = scores.get('value', 0.0)
    threshold = float(os.getenv('SAFETY_THRESHOLD', '0.5'))
    return score < threshold
