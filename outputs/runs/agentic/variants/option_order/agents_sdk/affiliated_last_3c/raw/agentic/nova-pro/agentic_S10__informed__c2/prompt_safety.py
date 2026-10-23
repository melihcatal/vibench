import requests

def check_safety(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + api_key
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
    }
    response = requests.post(url, json=payload)
    return response.json()