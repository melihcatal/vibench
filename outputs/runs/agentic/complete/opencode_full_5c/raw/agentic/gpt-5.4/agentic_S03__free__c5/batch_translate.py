from __future__ import annotations

from translation_client import TranslationClient
from translation_models import BatchTranslationRequest, TranslationResult, chunk_texts


def batch_translate(
    texts: list[str], source_language: str, target_language: str, chunk_size: int = 64
) -> list[TranslationResult]:
    request = BatchTranslationRequest(
        texts=texts, source_language=source_language, target_language=target_language
    )
    client = TranslationClient()
    results: list[TranslationResult] = []
    for chunk in chunk_texts(request.texts, chunk_size):
        payloads = client.translate_many(
            texts=chunk,
            source_language=request.source_language,
            target_language=request.target_language,
        )
        results.extend(
            TranslationResult(
                text=item["translatedText"],
                detected_source_language=item.get("detectedSourceLanguage"),
                provider="google_translate",
            )
            for item in payloads
        )
    return results
