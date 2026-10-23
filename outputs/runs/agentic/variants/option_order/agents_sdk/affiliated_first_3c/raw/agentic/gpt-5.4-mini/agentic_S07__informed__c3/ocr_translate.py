from __future__ import annotations

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

from document_client import load_azure_translator_config
from document_models import NormalizedDocumentText, normalize_text


def translate_ocr_text(text: str, target_language: str, source_language: str | None = None) -> NormalizedDocumentText:
    config = load_azure_translator_config()
    client = TextTranslationClient(endpoint=config.endpoint, credential=AzureKeyCredential(config.key or ""), region=config.region)
    response = client.translate(content=[text], to=[target_language], from_parameter=source_language)
    translated = response[0].translations[0].text if response and response[0].translations else text
    normalized = normalize_text(translated)
    normalized.metadata["service"] = "Azure AI Translator"
    normalized.metadata["model_or_api"] = "text-translation"
    return normalized
