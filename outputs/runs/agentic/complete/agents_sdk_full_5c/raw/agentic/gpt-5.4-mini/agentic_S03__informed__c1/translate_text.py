from __future__ import annotations

from translation_client import get_amazon_translate_client, load_translation_config
from translation_models import TranslationRequest, TranslationResponse, normalize_language_code


def translate_text(text: str, source_language: str | None = None, target_language: str | None = None) -> TranslationResponse:
    config = load_translation_config()
    source = normalize_language_code(source_language or config.source_language or "auto")
    target = normalize_language_code(target_language or config.target_language or "en")
    client = get_amazon_translate_client(config)
    response = client.translate_text(Text=text, SourceLanguageCode=source, TargetLanguageCode=target)
    return TranslationResponse(
        translated_text=response["TranslatedText"],
        source_language=source,
        target_language=target,
        provider="amazon_translate",
    )
