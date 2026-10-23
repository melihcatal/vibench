import os
import requests

TISANE_API_KEY = os.getenv('TISANE_API_KEY')

def moderate_batch(texts):
    url = 'https://api.tisane.ai/v1/moderation'
    headers = {'Authorization': f'Bearer {TISANE_API_KEY}', 'Content-Type': 'application/json'}
    payload = {'texts': texts}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()