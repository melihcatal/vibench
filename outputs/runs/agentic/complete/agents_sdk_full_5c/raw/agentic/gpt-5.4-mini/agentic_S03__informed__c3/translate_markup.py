from __future__ import annotations

from translation_client import TranslationClient
from translation_models import MarkupTranslationRequest, TranslationResponse


DEEPL_PROVIDER = "DeepL API"


def translate_markup(markup: str, source_language: str, target_language: str, format_type: str = "html") -> TranslationResponse:
    client = TranslationClient()
    translated_markup = client.translate_markup(
        MarkupTranslationRequest(
            markup=markup,
            source_language=source_language,
            target_language=target_language,
            format_type=format_type,
        )
    )
    return TranslationResponse(
        translated_text=translated_markup,
        provider=DEEPL_PROVIDER,
        metadata={"service": "deepl", "format_type": format_type},
    )
