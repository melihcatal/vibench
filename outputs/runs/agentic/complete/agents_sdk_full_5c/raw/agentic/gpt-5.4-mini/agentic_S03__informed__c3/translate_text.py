from __future__ import annotations

from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse


DEEPL_PROVIDER = "DeepL API"


def translate_text(text: str, source_language: str, target_language: str) -> TranslationResponse:
    client = TranslationClient()
    translated_text = client.translate_text(
        TranslationRequest(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )
    )
    return TranslationResponse(
        translated_text=translated_text,
        provider=DEEPL_PROVIDER,
        metadata={"service": "deepl", "provider_sdk": "deepl.Translator"},
    )
