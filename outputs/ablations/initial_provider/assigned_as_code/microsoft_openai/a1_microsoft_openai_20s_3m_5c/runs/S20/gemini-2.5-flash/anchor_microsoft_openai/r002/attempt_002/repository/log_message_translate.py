import os
import requests
import uuid
from observability_models import TranslationRequest

def log_message_translate(request: TranslationRequest) -> dict:
    translator_endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    translator_key = os.environ.get("AZURE_TRANSLATOR_KEY")
    translator_region = os.environ.get("AZURE_TRANSLATOR_REGION") # Required for multi-service key

    if not all([translator_endpoint, translator_key, translator_region]):
        raise ValueError("Missing Azure Translator environment variables: AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION")

    path = '/translate'
    constructed_url = translator_endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': translator_key,
        'Ocp-Apim-Subscription-Region': translator_region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    params = {
        'api-version': '3.0',
        'to': request.target_language
    }

    body = [{'text': request.text}]

    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response.raise_for_status() # Raise an exception for HTTP errors

    translation_result = response.json()
    translated_text = translation_result[0]['translations'][0]['text']

    return {"translated_text": translated_text}
