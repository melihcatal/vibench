import os

class SafetyClient:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.base_url = 'https://api.openai.com/v1'

    def call_api(self, endpoint, payload):
        import requests
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.post(f'{self.base_url}/{endpoint}', headers=headers, json=payload)
        return response.json()