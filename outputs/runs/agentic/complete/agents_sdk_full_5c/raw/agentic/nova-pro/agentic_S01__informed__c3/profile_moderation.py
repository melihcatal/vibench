import requests

def moderate_profile_text(text):
    api_key = 'YOUR_PERSPECTIVE_API_KEY'
    response = requests.post(
        'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze',
        json={
            'comment': {'text': text},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {} }
        },
        params={'key': api_key}
    )
    return response.json()