import os
import requests
import uuid

AZURE_TRANSLATOR_ENDPOINT = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
AZURE_TRANSLATOR_KEY = os.environ.get("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_REGION = os.environ.get("AZURE_TRANSLATOR_REGION") # e.g., "global" or "westus2"

def translate_text(text: str, target_language: str, source_language: str = "en") -> str:
    if not AZURE_TRANSLATOR_ENDPOINT or not AZURE_TRANSLATOR_KEY or not AZURE_TRANSLATOR_REGION:
        raise ValueError("AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION environment variables must be set.")
    
    path = '/translate'
    constructed_url = AZURE_TRANSLATOR_ENDPOINT + path

    params = {
        'api-version': '3.0',
        'from': source_language,
        'to': [target_language]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': AZURE_TRANSLATOR_REGION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    
    if request.status_code != 200:
        raise Exception(f"Azure Translator API error: {response}")

    return response[0]['translations'][0]['text']
