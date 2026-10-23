import os
import requests

def check_prompt_safety(text: str) -> dict:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        raise ValueError('PERSPECTIVE_API_KEY environment variable is required.')
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}'
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
            'IDENTITY_ATTACK': {}
        },
        'languages': ['en']
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    scores = {
        k: result['attributeScores'][k]['summaryScore']['value']
        for k in result['attributeScores']
    }
    is_unsafe = any(s > 0.7 for s in scores.values())
    return {'safe': not is_unsafe, 'scores': scores}
