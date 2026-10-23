import os
import requests
import json

def vendor_text_safety(text: str) -> dict:
    api_key = os.environ['PERSPECTIVE_API_KEY']
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}'
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANE': {},
            'THREAT': {}
        },
        'doNotStore': True
    }
    response = requests.post(url, json=payload)
    result = response.json()
    scores = {
        attr: result['attributeScores'][attr]['summaryScore']['value']
        for attr in payload['requestedAttributes']
    }
    is_safe = all(score < 0.5 for score in scores.values())
    return {'safe': is_safe, 'scores': scores}
