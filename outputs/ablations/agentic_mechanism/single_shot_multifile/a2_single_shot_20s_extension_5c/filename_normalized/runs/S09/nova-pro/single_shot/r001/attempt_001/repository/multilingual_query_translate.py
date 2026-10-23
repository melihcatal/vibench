import os
import requests

def translate_query(query, target_language):
    api_key = os.getenv('TRANSLATION_API_KEY')
    api_url = 'https://api.translationservice.com/v1/translate'
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    payload = {'text': query, 'target': target_language}
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['translated_text']