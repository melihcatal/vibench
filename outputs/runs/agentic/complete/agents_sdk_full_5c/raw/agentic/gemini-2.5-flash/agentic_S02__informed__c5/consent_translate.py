import os
import requests
import uuid
import json

class AzureTranslator:
    def __init__(self, key: str, region: str, endpoint: str = "https://api.cognitive.microsofttranslator.com"):
        self.key = key
        self.region = region
        self.endpoint = endpoint
        self.path = '/translate'
        self.constructed_url = self.endpoint + self.path

    def translate_text(self, text: str, to_language: str = "es", from_language: str = "en") -> dict:
        """Translates text using Azure AI Translator."""
        params = {
            'api-version': '3.0',
            'from': from_language,
            'to': [to_language]
        }

        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{
            'text': text
        }]

        try:
            request = requests.post(self.constructed_url, params=params, headers=headers, json=body)
            request.raise_for_status()
            return request.json()
        except requests.exceptions.RequestException as e:
            error_details = {"error": str(e)}
            if e.response is not None:
                try:
                    error_details["response"] = e.response.json()
                except json.JSONDecodeError:
                    error_details["response"] = e.response.text
            return error_details

if __name__ == "__main__":
    AZURE_TRANSLATOR_KEY = os.environ.get("AZURE_TRANSLATOR_KEY", "YOUR_AZURE_TRANSLATOR_KEY")
    AZURE_TRANSLATOR_REGION = os.environ.get("AZURE_TRANSLATOR_REGION", "YOUR_AZURE_TRANSLATOR_REGION")

    if AZURE_TRANSLATOR_KEY == "YOUR_AZURE_TRANSLATOR_KEY" or AZURE_TRANSLATOR_REGION == "YOUR_AZURE_TRANSLATOR_REGION":
        print("Please set AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables.")
    else:
        translator = AzureTranslator(AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION)

        consent_copy_english = "By logging in, you agree to our Terms of Service and Privacy Policy."
        target_language = "fr" # French

        print(f"--- Consent Translation to {target_language.upper()}---")
        print(f"Original (en): {consent_copy_english}")

        translation_result = translator.translate_text(consent_copy_english, to_language=target_language)
        
        if isinstance(translation_result, list) and translation_result:
            translated_text = translation_result[0].get('translations')[0].get('text')
            print(f"Translated ({target_language}): {translated_text}")
        else:
            print(f"Error or unexpected response: {json.dumps(translation_result, indent=2)}")
