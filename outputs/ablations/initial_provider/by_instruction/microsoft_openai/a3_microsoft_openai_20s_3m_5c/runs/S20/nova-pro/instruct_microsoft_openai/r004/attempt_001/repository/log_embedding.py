import os
import requests

AZURE_TEXT_ANALYTICS_ENDPOINT = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
AZURE_TEXT_ANALYTICS_KEY = os.getenv('AZURE_TEXT_ANALYTICS_KEY')

def embed_text(text):
    url = f'{AZURE_TEXT_ANALYTICS_ENDPOINT}/text/analytics/v3.1/languages'
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_TEXT_ANALYTICS_KEY,
        'Content-Type': 'application/json',
    }
    payload = {
        'documents': [\n            {\n                'language': 'en',\n                'id': '1',\n                'text': text,\n            },\n        ],\n    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

if __name__ == '__main__':\n    text = 'This is a sample log message.'
    embedding = embed_text(text)
    print(json.dumps(embedding, indent=2))
