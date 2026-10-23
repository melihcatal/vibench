from __future__ import annotations

from translation_client import azure_translate
from translation_models import (
    BatchTranslationRequest,
    TranslationResult,
    ensure_text_list,
    normalize_language_code,
)


def batch_translate(request: BatchTranslationRequest) -> list[TranslationResult]:
    source_language = normalize_language_code(request.source_language)
    target_language = normalize_language_code(request.target_language)
    payload = azure_translate(
        texts=ensure_text_list(request.texts),
        source_language=source_language,
        target_language=target_language,
        text_type="html" if request.content_type == "text/html" else "plain",
    )
    results: list[TranslationResult] = []
    for item in payload:
        translation = item["translations"][0]
        results.append(
            TranslationResult(
                text=translation["text"],
                provider="azure-ai-translator",
                source_language=source_language,
                target_language=target_language,
                detected_language=item.get("detectedLanguage", {}).get("language"),
                raw=item,
            )
        )
    return results
