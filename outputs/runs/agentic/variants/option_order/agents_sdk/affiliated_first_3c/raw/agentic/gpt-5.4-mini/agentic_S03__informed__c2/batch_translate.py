from __future__ import annotations

from translation_client import get_client, normalize_language_code
from translation_models import BatchTranslationRequest, BatchTranslationResult, normalize_text


def batch_translate(texts: list[str], source_language: str, target_language: str) -> BatchTranslationResult:
    client = get_client()
    request = BatchTranslationRequest(
        texts=[normalize_text(text) for text in texts],
        source_language=normalize_language_code(source_language),
        target_language=normalize_language_code(target_language),
    )
    translated_texts: list[str] = []
    for text in request.texts:
        response = client.translate(
            text,
            source_language=request.source_language,
            target_language=request.target_language,
            format_="text",
        )
        translated_texts.append(response["translatedText"])
    return BatchTranslationResult(
        translated_texts=translated_texts,
        source_language=request.source_language,
        target_language=request.target_language,
    )
