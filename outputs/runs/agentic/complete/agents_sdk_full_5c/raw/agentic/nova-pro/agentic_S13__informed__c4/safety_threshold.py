import requests

TISANE_API_KEY = 'your_tisane_api_key'

def apply_safety_threshold(text, threshold):
    url = 'https://api.tisane.ai/v1/threshold'
    headers = {'Authorization': f'Bearer {TISANE_API_KEY}'}
    payload = {'text': text, 'threshold': threshold}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()