import requests

PERSPECTIVE_API_KEY = 'your-perspective-api-key'

def moderate_batch(texts):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    payload = {
        'comments': [{'text': text} for text in texts],
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
    }
    headers = {'Content-Type': 'application/json', 'API-Key': PERSPECTIVE_API_KEY}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()