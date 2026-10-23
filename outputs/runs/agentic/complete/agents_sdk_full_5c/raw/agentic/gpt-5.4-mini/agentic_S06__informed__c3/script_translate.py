from __future__ import annotations

import os

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def translate_script(text: str, target_language: str = "en") -> str:
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
    key = os.environ.get("AZURE_TRANSLATOR_KEY", "")
    region = os.environ.get("AZURE_TRANSLATOR_REGION", "")
    if not key or not region:
        raise EnvironmentError("AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION are required")
    client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key), region=region)
    result = client.translate(content=[text], to=[target_language])
    return result[0].translations[0].text
