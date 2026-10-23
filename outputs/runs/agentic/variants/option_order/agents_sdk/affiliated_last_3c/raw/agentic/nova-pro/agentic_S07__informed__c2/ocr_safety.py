import requests

def check_text_safety(text):
    api_url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    api_key = 'YOUR_PERSPECTIVE_API_KEY'
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(api_url, params={'key': api_key}, json=payload)
    return response.json()