from __future__ import annotations

from typing import Optional

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

from document_models import TranslationResult, normalize_text


def translate_ocr_text(text: str, target_language: str, source_language: Optional[str] = None) -> TranslationResult:
    endpoint = "https://api.cognitive.microsofttranslator.com"
    key = __import__("os").environ["AZURE_TRANSLATOR_KEY"]
    region = __import__("os").environ["AZURE_TRANSLATOR_REGION"]
    client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key), region=region)
    response = client.translate(content=[normalize_text(text)], to=[target_language], from_parameter=source_language)
    translated = ""
    if response and response[0].translations:
        translated = response[0].translations[0].text
    return TranslationResult(translated_text=translated, raw=response)
