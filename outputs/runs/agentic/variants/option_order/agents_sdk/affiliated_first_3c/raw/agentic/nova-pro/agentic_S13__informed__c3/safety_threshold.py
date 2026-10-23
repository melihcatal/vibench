import requests

PERSPECTIVE_API_KEY = 'your-perspective-api-key'

def safety_threshold(text, threshold=0.5):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
    }
    headers = {'Content-Type': 'application/json', 'API-Key': PERSPECTIVE_API_KEY}
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    toxicity_score = result['attributeScores']['TOXICITY']['summaryScore']['value']
    return toxicity_score <= threshold