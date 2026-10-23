from typing import Dict, Any
import requests
import os

# Provider-specific: Google Cloud Translation API
# Model: google/cloud/translate_v2
# Environment variable: GOOGLE_CLOUD_TRANSLATE_API_KEY


class PayloadTranslator:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_CLOUD_TRANSLATE_API_KEY")
        self.api_url = f"https://translation.googleapis.com/language/translate/v2?key={self.api_key}"

    def translate_text(self, text: str, target_language: str) -> Dict[str, Any]:
        payload = {"q": text, "target": target_language}
        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()
        return response.json()
