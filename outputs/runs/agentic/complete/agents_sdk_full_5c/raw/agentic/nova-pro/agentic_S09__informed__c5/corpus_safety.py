import os
import requests

def check_corpus_safety(text):
    url = 'https://api.perspectiveapi.com/v1alpha1/commentanalyzer'
    headers = {'Content-Type': 'application/json', 'API_KEY': os.getenv('PERSPECTIVE_API_KEY')}
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if __name__ == '__main__':
    print(check_corpus_safety('sample text'))