from __future__ import annotations

from typing import List, Sequence

from translation_client import get_amazon_translate_client, load_translation_config
from translation_models import BatchTranslationResponse, normalize_language_code, normalize_text_segments


def batch_translate(texts: Sequence[str], source_language: str | None = None, target_language: str | None = None) -> BatchTranslationResponse:
    config = load_translation_config()
    source = normalize_language_code(source_language or config.source_language or "auto")
    target = normalize_language_code(target_language or config.target_language or "en")
    client = get_amazon_translate_client(config)
    translated: List[str] = []
    for text in normalize_text_segments(texts):
        result = client.translate_text(Text=text, SourceLanguageCode=source, TargetLanguageCode=target)
        translated.append(result["TranslatedText"])
    return BatchTranslationResponse(
        translated_texts=translated,
        source_language=source,
        target_language=target,
        provider="amazon_translate",
    )
