from typing import Dict, Any
import requests
import os

# Provider: Google Cloud Translation API
# Model/Service: translate (v2)
# API Endpoint: https://translation.googleapis.com/language/translate/v2
# Environment Variable: GOOGLE_APPLICATION_CREDENTIALS


class PayloadTranslator:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        self.endpoint = "https://translation.googleapis.com/language/translate/v2"

    def translate_text(self, text: str, target_language: str) -> Dict[str, Any]:
        """
        Translates customer-facing message payload text using Google Cloud Translation API.
        """
        params = {
            "q": text,
            "target": target_language,
            "format": "text",
            "key": self.api_key,
        }
        response = requests.post(self.endpoint, params=params)
        response.raise_for_status()
        return response.json()
