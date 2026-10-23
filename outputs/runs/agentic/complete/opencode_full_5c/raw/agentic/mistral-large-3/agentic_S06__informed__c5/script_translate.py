from typing import List, Dict, Any
import os
import requests


class AzureScriptTranslator:
    """Translate narration scripts using Azure AI Translator."""

    def __init__(self):
        self.key = os.getenv("AZURE_TRANSLATOR_KEY")
        self.region = os.getenv("AZURE_TRANSLATOR_REGION")
        self.endpoint = (
            f"https://api.cognitive.microsofttranslator.com/translate?api-version=3.0"
        )
        self.headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Ocp-Apim-Subscription-Region": self.region,
            "Content-Type": "application/json",
        }

    def translate(self, text: str, to_language: str, from_language: str = None) -> str:
        """Translate text to a target language."""
        params = {"to": to_language}
        if from_language:
            params["from"] = from_language

        body = [{"text": text}]
        response = requests.post(
            self.endpoint, headers=self.headers, params=params, json=body
        )
        response.raise_for_status()
        return response.json()[0]["translations"][0]["text"]
