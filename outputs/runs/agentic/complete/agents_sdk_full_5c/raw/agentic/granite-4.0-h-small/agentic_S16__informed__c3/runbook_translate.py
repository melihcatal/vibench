import os
import requests
from security_models import SecretPayloadModel

# Example using Google Gemini chat to translate runbook notes
# Endpoint: https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-001:chat/completed
# Requires environment variable GOOGLE_API_KEY

def translate_runbook_note(note: str, target_language: str = 'es') -> str:
    """Translate a secret rotation runbook note using Gemini chat API.

    Args:
        note (str): The original runbook note in source language.
        target_language (str): ISO 639-1 language code for the target language (default 'es').

    Returns:
        str: Translated note.
    """
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise RuntimeError('GOOGLE_API_KEY environment variable not set')

    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-001:chat/completed'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'}
    messages = [
        {'role': 'user', 'parts': [{'text': note}]},
        {'role': 'assistant', 'parts': [{'text': f'Please translate this into {target_language}.'}]}
    ]
    payload = {'messages': messages}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    answer = response.json()['candidates'][0]['parts'][0]['text']
    return answer
