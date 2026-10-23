import os
import requests
import uuid
import json

def translate_caption(text: str, target_language: str = "es"):
    """
    Translates a given text caption into a target language using Azure Translator Text API.
    """
    key = os.environ.get("AZURE_TRANSLATOR_TEXT_KEY")
    endpoint = os.environ.get("AZURE_TRANSLATOR_TEXT_ENDPOINT")
    region = os.environ.get("AZURE_TRANSLATOR_TEXT_REGION")

    if not key or not endpoint or not region:
        raise ValueError("AZURE_TRANSLATOR_TEXT_KEY, AZURE_TRANSLATOR_TEXT_ENDPOINT, and AZURE_TRANSLATOR_TEXT_REGION environment variables must be set.")

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'to': target_language
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    if request.status_code != 200:
        raise RuntimeError(f"Azure Translator API error: {response}")

    # The response is a list of dictionaries, each containing 'translations' which is another list
    # We expect one translation for the single text input
    if response and len(response) > 0 and 'translations' in response[0] and len(response[0]['translations']) > 0:
        return response[0]['translations'][0]['text']
    return ""
