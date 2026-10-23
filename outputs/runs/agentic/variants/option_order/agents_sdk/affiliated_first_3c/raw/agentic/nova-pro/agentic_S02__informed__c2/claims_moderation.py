import requests

PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

def moderate_claims(text):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
        'key': PERSPECTIVE_API_KEY,
    }
    response = requests.post(url, headers=headers, json=payload)
    moderation_result = response.json()
    print(moderation_result)