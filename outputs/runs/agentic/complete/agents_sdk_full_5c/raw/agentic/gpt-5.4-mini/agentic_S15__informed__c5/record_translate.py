from __future__ import annotations

from typing import Any, Dict

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

from database_models import NormalizedResponse


def translate_record_fields(text: str, to_language: str, from_language: str | None = None) -> NormalizedResponse:
    endpoint = __import__("os").environ["AZURE_TRANSLATOR_ENDPOINT"]
    key = __import__("os").environ["AZURE_TRANSLATOR_KEY"]
    region = __import__("os").environ["AZURE_TRANSLATOR_REGION"]
    client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key), region=region)
    result = client.translate(content=[text], to=[to_language], from_language=from_language)
    translated = result[0].translations[0].text if result and result[0].translations else ""
    return NormalizedResponse(ok=True, data={"translated_text": translated, "to_language": to_language})
