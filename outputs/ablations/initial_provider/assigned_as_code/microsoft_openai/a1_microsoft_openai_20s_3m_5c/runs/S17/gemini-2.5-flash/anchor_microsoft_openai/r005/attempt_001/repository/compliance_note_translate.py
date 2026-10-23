import os
import requests
import uuid

def translate_compliance_note(text: str, to_language: str, from_language: str = "en") -> dict:
    # Azure Translator Text API endpoint and key
    endpoint = os.environ.get("AZURE_TRANSLATOR_TEXT_ENDPOINT")
    key = os.environ.get("AZURE_TRANSLATOR_TEXT_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_TEXT_REGION")

    if not endpoint or not key or not region:
        raise ValueError("AZURE_TRANSLATOR_TEXT_ENDPOINT, AZURE_TRANSLATOR_TEXT_KEY, and AZURE_TRANSLATOR_TEXT_REGION environment variables must be set.")

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': from_language,
        'to': [to_language]
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

    translated_text = ""
    if response and isinstance(response, list) and len(response) > 0 and "translations" in response[0]:
        translated_text = response[0]["translations"][0]["text"]

    return {
        "original_text": text,
        "from_language": from_language,
        "to_language": to_language,
        "translated_text": translated_text
    }

# Example usage (requires AZURE_TRANSLATOR_TEXT_ENDPOINT, AZURE_TRANSLATOR_TEXT_KEY, AZURE_TRANSLATOR_TEXT_REGION env vars)
# note = "This note confirms compliance with data encryption standards."
# translated_note = translate_compliance_note(note, "fr")
# print(translated_note)
