import os
import requests

def moderate_transcript(transcript):
    api_key = os.environ.get('TISANE_API_KEY')
    url = 'https://api.tisane.ai/v1/moderate'
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {'text': transcript}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()