from __future__ import annotations

import os

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def translate_script(text: str, to_language: str, from_language: str | None = None) -> str:
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")
    if not key or not region:
        raise RuntimeError("AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION are required for Azure AI Translator")
    client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key), region=region)
    result = client.translate(content=[text], to=[to_language], from_parameter=from_language)
    return result[0].translations[0].text
