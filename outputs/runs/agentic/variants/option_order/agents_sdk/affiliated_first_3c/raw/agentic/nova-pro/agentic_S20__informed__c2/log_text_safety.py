import os
import requests

api_key = os.getenv('PERSPECTIVE_API_KEY')
url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + api_key

data = {
    'comment': {'text': 'This is a test log message.'},
    'languages': ['en'],
    'requestedAttributes': {'TOXICITY': {}},
}

response = requests.post(url, json=data)
print(response.json())