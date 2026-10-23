import os
import requests
import json
import uuid

def translate_text(text: str, target_language: str = "en", source_language: str = "auto"):
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    region = os.getenv("AZURE_TRANSLATOR_REGION")

    if not endpoint or not key or not region:
        raise ValueError("AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION environment variables not set.")

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'to': target_language
    }
    if source_language != "auto":
        params['from'] = source_language

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    try:
        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        response.raise_for_status()
        translation_result = response.json()
        translated_text = translation_result[0]['translations'][0]['text']
        return {"translated_text": translated_text, "full_response": translation_result}
    except requests.exceptions.RequestException as e:
        return {"error": f"Translation failed: {e}", "details": response.text if response else "No response"}
