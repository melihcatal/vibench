import requests
import uuid
import os

def translate_text(text: str, target_language: str = "en") -> str:
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    location = os.environ.get("AZURE_TRANSLATOR_LOCATION") # e.g., eastus

    if not key or not endpoint or not location:
        raise ValueError("AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_ENDPOINT, and AZURE_TRANSLATOR_LOCATION environment variables must be set.")

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'to': target_language
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    if request.status_code != 200:
        raise Exception(f"Translation failed with status code {request.status_code}: {response}")

    # Assuming a single translation for a single text input
    return response[0]['translations'][0]['text']

def translate_runbook_notes(notes: str, target_language: str = "en") -> str:
    return translate_text(notes, target_language)
