import os
import requests

TISANE_API_KEY = os.getenv('TISANE_API_KEY')

def moderate_batch(texts):
    url = 'https://api.tisane.ai/v1/moderate'
    headers = {'Authorization': 'Bearer ' + TISANE_API_KEY}
    payload = {'texts': texts}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()