import os
import requests
import uuid

def translate_record_field(text: str, target_language: str = "es", source_language: str = "en") -> str:
    azure_translator_endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    azure_translator_key = os.environ.get("AZURE_TRANSLATOR_KEY")
    azure_translator_region = os.environ.get("AZURE_TRANSLATOR_REGION") # e.g., westus2

    if not all([azure_translator_endpoint, azure_translator_key, azure_translator_region]):
        raise ValueError("Azure Translator environment variables not set. Please set AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION.")

    path = '/translate'
    constructed_url = azure_translator_endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': azure_translator_key,
        'Ocp-Apim-Subscription-Region': azure_translator_region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    params = {
        'api-version': '3.0',
        'from': source_language,
        'to': [target_language]
    }

    body = [{'text': text}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    if request.status_code == 200 and response:
        return response[0]['translations'][0]['text']
    else:
        print(f"Error translating text: {response}")
        return text # Return original text on failure
