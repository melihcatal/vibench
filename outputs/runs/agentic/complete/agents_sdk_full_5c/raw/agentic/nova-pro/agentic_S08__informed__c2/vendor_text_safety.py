import requests

def moderate_vendor_text(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    data = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
        'doNotStore': True
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers, params={'key': api_key})
    return response.json()