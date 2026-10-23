import os
import requests

api_key = os.getenv('TISANE_API_KEY')

def moderate_claims(claims):
    response = requests.post('https://api.tisane.ai/moderate', headers={'Authorization': f'Bearer {api_key}'}, json=claims)
    return response.json()