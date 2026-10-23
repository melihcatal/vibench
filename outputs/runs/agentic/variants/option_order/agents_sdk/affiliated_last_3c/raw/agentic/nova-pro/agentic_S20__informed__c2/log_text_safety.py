import os
import requests

API_KEY = os.getenv('PERSPECTIVE_API_KEY')
URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

data = {
    'comment': {'text': 'This is a log message'},
    'languages': ['en'],
    'requestedAttributes': {'TOXICITY': {}},
}
response = requests.post(URL, params={'key': API_KEY}, json=data)
print(response.json())