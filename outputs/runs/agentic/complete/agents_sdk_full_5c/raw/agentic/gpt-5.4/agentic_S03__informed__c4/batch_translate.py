from __future__ import annotations

from typing import List, Optional, Sequence

from translation_client import build_translation_client, normalize_translation_languages
from translation_models import BatchTranslationRequest, BatchTranslationResult, TranslationResult, chunk_iterable


def batch_translate(
    texts: Sequence[str],
    target_language: str,
    source_language: Optional[str] = None,
    mime_type: str = "text/plain",
    chunk_size: int = 50,
) -> BatchTranslationResult:
    client, parent, model_path = build_translation_client()
    source_language, target_language = normalize_translation_languages(source_language, target_language)
    request = BatchTranslationRequest(
        texts=texts,
        source_language=source_language,
        target_language=target_language,
        mime_type=mime_type,
    )

    ordered_results: List[TranslationResult] = []
    for chunk in chunk_iterable(request.normalized_texts(), chunk_size):
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": chunk,
                "mime_type": request.mime_type,
                "target_language_code": request.target_language,
                "source_language_code": request.source_language,
                "model": model_path,
            }
        )
        ordered_results.extend(
            TranslationResult(
                translated_text=item.translated_text,
                detected_language=getattr(item, "detected_language_code", None),
                provider="google-cloud-translate",
                model="general/nmt",
                raw=item,
            )
            for item in response.translations
        )

    return BatchTranslationResult(translations=ordered_results)
