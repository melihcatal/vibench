from __future__ import annotations

from translation_client import batch_translate_with_google
from translation_models import BatchTranslationRequest, TranslationResult, normalize_texts


def batch_translate(
    texts: list[str],
    target_language: str,
    source_language: str | None = None,
) -> list[TranslationResult]:
    request = BatchTranslationRequest(
        texts=normalize_texts(texts),
        source_language=source_language,
        target_language=target_language,
        content_type="text/plain",
    )
    raws = batch_translate_with_google(
        texts=request.texts,
        target_language=request.target_language,
        source_language=request.source_language,
        format_="text",
    )
    return [
        TranslationResult(
            translated_text=item["translatedText"],
            detected_source_language=item.get("detectedSourceLanguage") or request.source_language,
            provider="google_translate",
            model="google-cloud-translate-v2",
            raw=item,
        )
        for item in raws
    ]
