import os
import requests

class AzureTranslatorClient:
    def __init__(self, api_key=None, region=None, endpoint="https://api.cognitive.microsofttranslator.com"):
        self.api_key = api_key or os.environ.get("AZURE_TRANSLATOR_API_KEY")
        self.region = region or os.environ.get("AZURE_TRANSLATOR_REGION")
        self.endpoint = endpoint
        if not self.api_key or not self.region:
            raise ValueError("Azure Translator API key and region must be provided or set as environment variables.")

    def translate_request(self, text_entries, from_lang, to_lang, text_type='plain'):
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-type': 'application/json'
        }
        params = {
            'api-version': '3.0',
            'from': from_lang,
            'to': to_lang,
            'textType': text_type
        }
        body = [{'Text': entry} for entry in text_entries]
        
        response = requests.post(f"{self.endpoint}/translate", headers=headers, params=params, json=body, timeout=30)
        response.raise_for_status()
        return response.json()
