import os
import requests
import uuid

def translate_platform_output(text_output, target_locale, config=None):
    config = config or {}
    key = config.get("azure_translator_key", os.environ.get("AZURE_TRANSLATOR_KEY"))
    endpoint = config.get("azure_translator_endpoint", os.environ.get("AZURE_TRANSLATOR_ENDPOINT"))
    location = config.get("azure_translator_location", os.environ.get("AZURE_TRANSLATOR_LOCATION"))

    if not key or not endpoint or not location:
        print("Azure Translator key, endpoint, or location not configured. Skipping translation.")
        return {"translated_text": text_output, "source_locale": "en", "target_locale": target_locale}

    path = '/translate'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text_output
    }]

    params = {
        'api-version': '3.0',
        'to': target_locale
    }

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    if response and isinstance(response, list) and 'translations' in response[0]:
        translated_text = response[0]['translations'][0]['text']
        source_locale = response[0]['detectedLanguage']['language']
        return {"translated_text": translated_text, "source_locale": source_locale, "target_locale": target_locale}
    else:
        print(f"Translation failed: {response}")
        return {"translated_text": text_output, "source_locale": "en", "target_locale": target_locale}
