import requests

def check_corpus_safety(text):
    api_key = 'your-perspective-api-key'
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    params = {
        'key': api_key,
    }
    data = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
    }
    response = requests.post(url, params=params, json=data)
    return response.json()