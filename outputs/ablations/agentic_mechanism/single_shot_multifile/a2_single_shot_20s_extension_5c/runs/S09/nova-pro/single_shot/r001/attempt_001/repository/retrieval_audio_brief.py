import os
import requests

def generate_audio_brief(text):
    api_key = os.getenv('AUDIO_BRIEF_API_KEY')
    api_url = 'https://api.audiobrief.com/v1/generate'
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    payload = {'text': text}
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['audio_url']