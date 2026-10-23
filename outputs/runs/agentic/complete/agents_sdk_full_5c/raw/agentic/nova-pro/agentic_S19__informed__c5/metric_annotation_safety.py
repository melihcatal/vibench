import os
import requests

url = 'https://api.perspectiveapi.com/v1alpha1/commentAnalyzer'
api_key = os.getenv('PERSPECTIVE_API_KEY')

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

def check_annotation(annotation):
    payload = {
        'comment': {'text': annotation},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()