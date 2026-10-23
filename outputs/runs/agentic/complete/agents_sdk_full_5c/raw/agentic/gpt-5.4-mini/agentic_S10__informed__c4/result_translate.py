from __future__ import annotations

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from model_models import normalize_text


def translate_result(text: str, target_language: str, source_language: str | None = None) -> str:
    endpoint = __import__("os").getenv("AZURE_TRANSLATOR_ENDPOINT")
    key = __import__("os").getenv("AZURE_TRANSLATOR_KEY")
    region = __import__("os").getenv("AZURE_TRANSLATOR_REGION")
    client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key), region=region)
    result = client.translate(content=[text], to=[target_language], from_parameter=source_language)
    return normalize_text(result[0].translations[0].text)
