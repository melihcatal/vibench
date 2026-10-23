import os
import requests

PERSPECTIVE_ENDPOINT = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'


def corpus_safety(texts):
    key = os.getenv('PERSPECTIVE_API_KEY')
    results = []
    for text in texts:
        payload = {
            'comment': {'text': text},
            'requestedAttributes': {'TOXICITY': {}},
            'languages': ['en'],
        }
        response = requests.post(f'{PERSPECTIVE_ENDPOINT}?key={key}', json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        toxicity = data['attributeScores']['TOXICITY']['summaryScore']['value']
        results.append({'text': text, 'toxicity': toxicity, 'safe': toxicity < 0.5})
    return results
