import requests

def moderate_text(text):
    response = requests.post(
        'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze',
        json={
            'comment': {'text': text},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {} }
        },
        params={'key': 'YOUR_API_KEY'}
    )
    return response.json()