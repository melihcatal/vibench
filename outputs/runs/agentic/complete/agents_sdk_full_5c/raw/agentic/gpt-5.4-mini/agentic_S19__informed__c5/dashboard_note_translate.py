from __future__ import annotations

import os

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

from observability_models import TranslationRequest

PROVIDER = "Azure AI Translator"


def dashboard_note_translate(text: str, target_language: str, source_language: str | None = None) -> str:
    request = TranslationRequest(text=text, target_language=target_language, source_language=source_language)
    client = TextTranslationClient(endpoint=os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com"), credential=AzureKeyCredential(os.environ.get("AZURE_TRANSLATOR_KEY", "")))
    result = client.translate(content=[request.text], to=[request.target_language], from_parameter=request.source_language)
    return result[0].translations[0].text if result and result[0].translations else request.text
