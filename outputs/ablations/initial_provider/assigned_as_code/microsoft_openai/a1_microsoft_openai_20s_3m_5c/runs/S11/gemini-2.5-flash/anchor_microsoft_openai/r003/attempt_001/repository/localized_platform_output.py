import requests
import uuid
import os

def translate_platform_output(text: str, target_language: str, config: dict = None) -> dict:
    config = config or {}
    key = config.get("AZURE_TRANSLATOR_TEXT_KEY") or os.getenv("AZURE_TRANSLATOR_TEXT_KEY")
    endpoint = config.get("AZURE_TRANSLATOR_TEXT_ENDPOINT") or os.getenv("AZURE_TRANSLATOR_TEXT_ENDPOINT")
    location = config.get("AZURE_TRANSLATOR_TEXT_LOCATION") or os.getenv("AZURE_TRANSLATOR_TEXT_LOCATION")

    if not key or not endpoint or not location:
        raise ValueError("Azure Translator Text API key, endpoint, and location not found in config or environment variables.")

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
        'to': target_language
    }

    body = [{'text': text}]

    try:
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = request.json()
        
        if request.status_code == 200 and response and len(response) > 0 and 'translations' in response[0] and len(response[0]['translations']) > 0:
            translated_text = response[0]['translations'][0]['text']
            return {"translated_text": translated_text}
        else:
            return {"error": "Translation failed or returned empty response.", "response": response}

    except Exception as e:
        return {"error": str(e)}
