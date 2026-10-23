import requests

def check_payload_safety(text):
    api_key = 'YOUR_PERSPECTIVE_API_KEY'
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + api_key
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
    }
    response = requests.post(url, json=payload)
    return response.json()