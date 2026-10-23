import os
import requests
import uuid
import json
from typing import List, Dict, Any

# Azure Translator Text API
from identity_client import FederatedLoginConfig

AZURE_TRANSLATOR_KEY = FederatedLoginConfig.AZURE_TRANSLATOR_KEY
AZURE_TRANSLATOR_ENDPOINT = FederatedLoginConfig.AZURE_TRANSLATOR_ENDPOINT
AZURE_TRANSLATOR_REGION = FederatedLoginConfig.AZURE_TRANSLATOR_REGION

def translate_consent_text(text_to_translate: str, to_language: str = "es", from_language: str = "en") -> Dict[str, Any]:
    """Translates consent copy using Azure Translator Text API."""
    if not AZURE_TRANSLATOR_KEY or AZURE_TRANSLATOR_KEY == "YOUR_AZURE_TRANSLATOR_KEY":
        print("Azure Translator API key is not set. Please set AZURE_TRANSLATOR_KEY environment variable.")
        return {"error": "Azure Translator API key not configured"}

    path = '/translate'
    constructed_url = AZURE_TRANSLATOR_ENDPOINT + path

    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': AZURE_TRANSLATOR_REGION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    params = {
        'api-version': '3.0',
        'from': from_language,
        'to': [to_language]
    }

    body = [{'text': text_to_translate}]

    try:
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        request.raise_for_status()
        response = request.json()
        
        if response and isinstance(response, list) and len(response) > 0 and 'translations' in response[0]:
            translated_text = response[0]['translations'][0]['text']
            detected_language = response[0].get('detectedLanguage', {}).get('language')
            return {
                "original_text": text_to_translate,
                "from_language_detected": detected_language or from_language,
                "to_language": to_language,
                "translated_text": translated_text
            }
        return {"error": "Unexpected response format", "raw_response": response}

    except requests.exceptions.RequestException as e:
        print(f"Error calling Azure Translator Text API: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    example_consent_copy = "By clicking 'Accept', you agree to our Terms of Service and Privacy Policy. Your personal data will be processed according to our data retention policy."
    target_language = "fr"

    print(f"Translating consent copy to '{target_language}'...")
    translation_result = translate_consent_text(example_consent_copy, to_language=target_language)
    print(json.dumps(translation_result, indent=2))

    example_german_copy = "Mit dem Klick auf 'Akzeptieren' stimmen Sie unseren Allgemeinen Geschäftsbedingungen und unserer Datenschutzerklärung zu."
    target_language_english = "en"
    print(f"\nTranslating German consent copy to '{target_language_english}'...")
    translation_result_german = translate_consent_text(example_german_copy, from_language="de", to_language=target_language_english)
    print(json.dumps(translation_result_german, indent=2))
