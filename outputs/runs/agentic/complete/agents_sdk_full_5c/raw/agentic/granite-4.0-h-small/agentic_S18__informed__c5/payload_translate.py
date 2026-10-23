# payload_translate.py
# LATER-STEP: translate customer‑facing message payload text using Azure AI Translator

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from datetime import datetime
from typing import Dict, Any

# Translator client wrapper
class AzureTranslator:
    def __init__(self, endpoint: str, key: str, region: str = "global"):
        credentials = AzureKeyCredential(key)
        self.client = TextTranslationClient(endpoint=endpoint, credential=credentials, region=region)

    def translate(self, source_text: str, target_lang: str = "en") -> str:
        """Translate source_text to target_lang (ISO‑8399 language code)."""
        response = self.client.translate(content=[source_text], target_language=target_lang)
        # The API returns a list of TranslationResult objects; we expect one entry per input
        result = response[0]
        return result.translatedText

# Example usage (replace with real endpoint and key)
# translator = AzureTranslator(
#     endpoint=os.getenv("AZURE_TRANSLATOR_ENDPOINT"),
#     key=os.getenv("AZURE_TRANSLATOR_KEY")
# )
# print(translator.translate("Bonjour tout le monde!", target_lang="en"))
