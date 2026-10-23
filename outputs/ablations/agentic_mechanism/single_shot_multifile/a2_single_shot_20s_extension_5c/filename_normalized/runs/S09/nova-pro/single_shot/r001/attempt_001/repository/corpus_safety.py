import os
import requests

def check_corpus_safety(text):
    api_key = os.getenv('SAFETY_API_KEY')
    api_url = 'https://api.safetycheck.com/v1/check'
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    payload = {'text': text}
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['is_safe']