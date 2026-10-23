import requests

TISANE_API_KEY = 'your_tisane_api_key'

def moderate_batch(texts):
    url = 'https://api.tisane.ai/v1/moderate_batch'
    headers = {'Authorization': f'Bearer {TISANE_API_KEY}'}
    payload = {'texts': texts}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()