import os
import requests

TISANE_API_KEY = os.getenv('TISANE_API_KEY')

def moderate_batch(texts):
    url = 'https://api.tisane.ai/v1/moderation'
    headers = {'Authorization': f'Bearer {TISANE_API_KEY}'}
    payload = {'texts': texts}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()