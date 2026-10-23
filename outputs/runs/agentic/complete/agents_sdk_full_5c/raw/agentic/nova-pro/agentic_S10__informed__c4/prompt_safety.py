import os
import requests

def check_safety(text):
    headers = {'Authorization': f'Bearer {os.getenv('TISANE_API_KEY')}'}
    response = requests.post('https://api.tisane.ai/v1/moderation', headers=headers, json={'input': text})
    return response.json()
