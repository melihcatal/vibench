from __future__ import annotations

from typing import Optional

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def translate_payload_text(text: str, target_language: str, endpoint: Optional[str] = None, key: Optional[str] = None) -> str:
    client = TextTranslationClient(
        endpoint=endpoint or __import__("os").getenv("AZURE_TRANSLATOR_ENDPOINT", ""),
        credential=AzureKeyCredential(key or __import__("os").getenv("AZURE_TRANSLATOR_KEY", "")),
        region=__import__("os").getenv("AZURE_TRANSLATOR_REGION", ""),
    )
    result = client.translate(content=[text], to=[target_language])
    return result[0].translations[0].text if result and result[0].translations else text
