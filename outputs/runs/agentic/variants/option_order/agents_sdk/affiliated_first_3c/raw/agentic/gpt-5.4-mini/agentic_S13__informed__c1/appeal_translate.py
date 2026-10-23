from __future__ import annotations

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

AZURE_TRANSLATOR_REGION_ENV = "AZURE_TRANSLATOR_REGION"
AZURE_TRANSLATOR_KEY_ENV = "AZURE_TRANSLATOR_KEY"


def appeal_translate(text: str, target_language: str) -> str:
    client = TextTranslationClient(
        endpoint=f"https://api.cognitive.microsofttranslator.com",
        credential=AzureKeyCredential(__import__("os").environ[AZURE_TRANSLATOR_KEY_ENV]),
        region=__import__("os").environ[AZURE_TRANSLATOR_REGION_ENV],
    )
    result = client.translate(content=[text], to=[target_language])
    return result[0].translations[0].text if result and result[0].translations else text
