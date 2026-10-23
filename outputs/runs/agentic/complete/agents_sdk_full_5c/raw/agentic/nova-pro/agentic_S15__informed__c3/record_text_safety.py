import requests

PERSPECTIVE_API_KEY = 'your-perspective-api-key'

def check_text_safety(text):
    response = requests.post(
        'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + PERSPECTIVE_API_KEY,
        json={
            'comment': {'text': text},
            'requestedAttributes': {'TOXICITY': {}},
            'languages': ['en']
        }
    )
    return response.json()