from __future__ import annotations

import os

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def translate_script(text: str, target_language: str, source_language: str | None = None) -> str:
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
    key = os.environ["AZURE_TRANSLATOR_KEY"]
    region = os.environ["AZURE_TRANSLATOR_REGION"]
    client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key), region=region)
    kwargs = {"to": [target_language]}
    if source_language:
        kwargs["from"] = source_language
    result = client.translate(content=[text], **kwargs)
    return result[0].translations[0].text
