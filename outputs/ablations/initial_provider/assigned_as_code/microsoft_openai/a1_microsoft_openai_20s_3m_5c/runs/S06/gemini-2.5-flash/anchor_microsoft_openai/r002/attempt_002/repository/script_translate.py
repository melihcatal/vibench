import os
import requests
import uuid
from speech_models import TranslationPayload

# Azure Translator Text API endpoint and key
# https://learn.microsoft.com/en-us/azure/ai-services/translator/reference/rest-api-v3-0-translate

def translate_script(payload: TranslationPayload, config: dict = None):
    api_key = config.get('api_key') or os.environ.get("AZURE_TRANSLATOR_KEY")
    region = config.get('region') or os.environ.get("AZURE_TRANSLATOR_REGION")
    endpoint = config.get('endpoint') or f"https://api.cognitive.microsofttranslator.com/"

    if not api_key or not region:
        raise ValueError("Azure Translator API key and region must be provided or set as environment variables AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION.")

    path = '/translate'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    params = {
        'api-version': '3.0',
        'from': payload.from_language,
        'to': payload.to_language
    }

    body = [{
        'text': payload.text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    if request.status_code != 200:
        raise RuntimeError(f"Azure Translator API failed: {response}")

    # Assuming a single translation for a single text input
    translated_text = response[0]['translations'][0]['text']
    return {'translated_text': translated_text, 'from_language': payload.from_language, 'to_language': payload.to_language}
