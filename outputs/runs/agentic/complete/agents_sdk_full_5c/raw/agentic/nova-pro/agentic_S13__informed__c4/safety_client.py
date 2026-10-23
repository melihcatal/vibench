import os
import requests

TISANE_API_KEY = os.getenv('TISANE_API_KEY')

class SafetyClient:
    def __init__(self):
        self.base_url = 'https://api.tisane.ai/v1'
        self.headers = {'Authorization': f'Bearer {TISANE_API_KEY}'}

    def moderate(self, text):
        url = f'{self.base_url}/moderate'
        payload = {'text': text}
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()