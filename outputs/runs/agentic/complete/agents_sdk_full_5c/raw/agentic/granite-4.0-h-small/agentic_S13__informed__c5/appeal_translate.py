# appeal_translate.py
import os
import json
from safety_client import TextSafetyClient

# Azure Translator Text endpoint and key (requires env vars)
AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
if not AZURE_TRANSLATOR_ENDPOINT or not AZURE_TRANSLATOR_KEY:
    raise RuntimeError("Set AZURE_TRANSLATOR_ENDPOINT and AZURE_TRANSLATOR_KEY environment variables")

HEADERS = {
    "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
    "Content-Type": "application/json"
}

class AppealTranslator:
    """Helper for translating appeal text into a reviewer-friendly language.",
    "Uses Azure Translator Text to translate the appeal from the user's language to English (or any target language)."""
    def __init__(self, target_lang: str = "en"):
        self.target_lang = target_lang
        self.base_url = AZURE_TRANSLATOR_ENDPOINT
        self.session = requests.Session()

    def translate(self, text: str, source_lang: str | None = None) -> str:
        """Translates a single string."""
        payload = [{"Text": text}]  # list of dicts as required by the API
        params = {
            "api-version": "3.0",
            "to": [self.target_lang]
        }
        if source_lang:
            params["from"] = source_lang
        response = self.session.post(
            f"{self.base_url}/translate",
            headers=HEADERS,
            params=params,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        # Result format: [{'translations': [{'text': ..., 'to': 'en'}]}]
        return result[0]["translations"][0]["text"]

if __name__ == "__main__":
    # Quick demo – requires AZURE_TRANSLATOR_ENDPOINT and AZURE_TRANSLATOR_KEY env vars
    appeal = "Por favor, explique por qué este contenido está mal."
    translator = AppealTranslator(target_lang="en")
    translated = translator.translate(appeal)
    print("Original:", appeal)
    print("Translated:", translated)