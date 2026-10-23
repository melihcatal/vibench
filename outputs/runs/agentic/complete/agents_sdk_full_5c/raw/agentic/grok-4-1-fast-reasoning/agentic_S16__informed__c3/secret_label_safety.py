import requests
import os

def check_secret_label_safety(label: str, notes: str) -> dict:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}'
    text = f'{label}: {notes}'
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        },
        'languages': ['en']
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()['attributeScores']
