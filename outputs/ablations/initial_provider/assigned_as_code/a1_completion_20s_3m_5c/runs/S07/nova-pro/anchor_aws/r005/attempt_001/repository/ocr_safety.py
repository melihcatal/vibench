import os
import requests


def check_safety(text: str) -> bool:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
        'key': api_key
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    toxicity_score = response.json()['attributeScores']['TOXICITY']['summaryScore']['value']
    return toxicity_score < 0.5