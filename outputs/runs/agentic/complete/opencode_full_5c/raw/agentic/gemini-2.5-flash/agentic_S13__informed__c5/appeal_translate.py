import os
import requests
import uuid

AZURE_TRANSLATOR_KEY = os.environ.get("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_REGION = os.environ.get("AZURE_TRANSLATOR_REGION")
AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"


class AzureAppealTranslator:
    def __init__(self):
        if not AZURE_TRANSLATOR_KEY or not AZURE_TRANSLATOR_REGION:
            raise ValueError(
                "Azure Translator key and region must be set in environment variables."
            )
        self.key = AZURE_TRANSLATOR_KEY
        self.region = AZURE_TRANSLATOR_REGION
        self.endpoint = AZURE_TRANSLATOR_ENDPOINT

    def translate_appeal_text(self, text: str, target_language: str = "en") -> str:
        """Translate appeal text for review using Azure AI Translator."""
        path = "/translate"
        constructed_url = self.endpoint + path

        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Ocp-Apim-Subscription-Region": self.region,
            "Content-type": "application/json",
            "X-ClientTraceId": str(uuid.uuid4()),
        }

        params = {"api-version": "3.0", "to": target_language}

        body = [{"text": text}]

        response = requests.post(
            constructed_url, params=params, headers=headers, json=body
        )
        response.raise_for_status()
        translated_text = response.json()[0]["translations"][0]["text"]
        return translated_text
