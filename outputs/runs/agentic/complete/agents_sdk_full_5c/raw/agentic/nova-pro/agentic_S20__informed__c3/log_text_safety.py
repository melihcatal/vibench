import requests

PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

headers = {'Content-Type': 'application/json'}
data = {
    'comment': {'text': 'log message to check'},
    'requestedAttributes': {'TOXICITY': {}},
    'languages': ['en']
}

response = requests.post(url, headers=headers, params={'key': PERSPECTIVE_API_KEY}, json=data)