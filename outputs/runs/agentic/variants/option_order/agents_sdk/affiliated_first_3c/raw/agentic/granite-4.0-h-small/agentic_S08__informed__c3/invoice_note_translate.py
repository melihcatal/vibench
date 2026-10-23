import os
import requests

# Azure AI Translator (REST) – provider identifiable by endpoint and credentials
AZURE_TRANSLATOR_ENDPOINT = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'
AZURE_TRANSLATOR_KEY = os.getenv('AZURE_TRANSLATOR_KEY')

def translate_notes(note: str, target_lang: str = 'es') -> str:
    """Translate extracted invoice notes using Azure Translator and return translated text."""
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_TRANSLATOR_KEY,
        'Content-Type': 'application/json'
    }
    body = [{ 'Text': note }]
    resp = requests.post(AZURE_TRANSLATOR_ENDPOINT, headers=headers, json=body)
    resp.raise_for_status()
    translated = resp.json()[0]['translations'][0]['Text']
    return translated