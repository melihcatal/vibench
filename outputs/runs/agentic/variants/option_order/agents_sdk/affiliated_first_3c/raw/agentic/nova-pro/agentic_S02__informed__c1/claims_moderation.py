import requests

def moderate_claims(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}},
        'languages': ['en']
    }
    headers = {'Content-Type': 'application/json', 'API-Key': api_key}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()