import requests

PERSPECTIVE_API_KEY = 'your-perspective-api-key'

def redact_unsafe(text):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
    }
    headers = {'Content-Type': 'application/json', 'API-Key': PERSPECTIVE_API_KEY}
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    if result['attributeScores']['TOXICITY']['summaryScore']['value'] > 0.5:
        return '[REDACTED]'
    return text