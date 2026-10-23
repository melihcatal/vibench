import os
import requests

TISANE_API_KEY = os.getenv('TISANE_API_KEY')

def redact_unsafe(text):
    url = 'https://api.tisane.io/v1/moderate'
    headers = {'Authorization': 'Bearer ' + TISANE_API_KEY}
    payload = {'text': text}
    response = requests.post(url, json=payload, headers=headers)
    if response.json().get('toxicity_score') > 0.5:
        return '[REDACTED]'
    return text
