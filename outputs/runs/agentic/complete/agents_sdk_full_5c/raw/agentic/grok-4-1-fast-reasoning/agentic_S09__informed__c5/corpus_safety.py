import os
import requests

def check_corpus_safety(texts: list[str]) -&gt; list[dict]:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        raise ValueError('PERSPECTIVE_API_KEY required')
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}'
    results = []
    for text in texts:
        payload = {
            'comment': {'text': text},
            'requestedAttributes': {
                'TOXICITY': {},
                'SEVERE_TOXICITY': {},
                'INSULT': {},
                'PROFANITY': {}
            },
            'languages': ['en']
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        results.append(response.json())
    return results