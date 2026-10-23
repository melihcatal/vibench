import requests
import uuid
import os

def localized_platform_output(text_output, target_locale, config=None):
    config = config or {}
    key = os.environ.get("AZURE_TRANSLATOR_TEXT_KEY", config.get("key"))
    endpoint = os.environ.get("AZURE_TRANSLATOR_TEXT_ENDPOINT", config.get("endpoint"))
    location = os.environ.get("AZURE_TRANSLATOR_TEXT_LOCATION", config.get("location")) # e.g., "global" or a specific region

    if not all([key, endpoint, location]):
        raise ValueError("Azure Translator Text key, endpoint, and location must be provided.")

    path = '/translate'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    params = {
        'api-version': '3.0',
        'to': target_locale
    }

    body = [{'text': text_output}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    if request.status_code != 200:
        raise Exception(f"Translation failed with status code {request.status_code}: {response}")

    translated_text = response[0]['translations'][0]['text']
    return {"translated_text": translated_text, "source_text": text_output, "target_locale": target_locale}
