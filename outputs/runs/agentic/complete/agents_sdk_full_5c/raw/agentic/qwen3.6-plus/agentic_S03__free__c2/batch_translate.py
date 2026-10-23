"""
batch_translate.py - Translates a list of strings while preserving order
using Google Cloud Translation API v3.
"""

from typing import List, Optional
from google.cloud import translate_v3 as translate

from translation_client import get_translation_client, get_project_location, validate_client_ready
from translation_models import (
    TranslationResult,
    BatchTranslationResult,
    normalize_language_code,
    validate_translation_response,
)


def batch_translate(
    texts: List[str],
    source_language: str = "auto",
    target_language: str = "es",
    model: str = "nmt",
    batch_size: int = 128,
) -> BatchTranslationResult:
    """
    Translate a list of strings using Google Cloud Translation API v3,
    preserving the order of the input list.

    Google Cloud Translation supports batching up to 128 text segments per
    request. Larger lists are chunked automatically.

    Args:
        texts: List of text strings to translate.
        source_language: Source language code (BCP-47). Use "auto" for detection.
        target_language: Target language code (BCP-47).
        model: Translation model identifier ("nmt" or "base" for Google Cloud NMT).
        batch_size: Maximum number of texts per API call (Google limit is 128).

    Returns:
        BatchTranslationResult with all translated segments in original order.
    """
    if not validate_client_ready():
        raise RuntimeError(
            "Google Cloud Translation client not configured. "
            "Set GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS."
        )

    if not texts:
        return BatchTranslationResult(
            results=[],
            source_texts=[],
            target_language=target_language,
            total_count=0,
        )

    source_lang = normalize_language_code(source_language)
    target_lang = normalize_language_code(target_language)

    client = get_translation_client()
    parent = get_project_location()

    model_path = f"{parent}/models/{model}" if model != "nmt" else None

    all_results: List[TranslationResult] = []
    effective_batch_size = min(batch_size, 128)  # Google Cloud Translation API limit

    for i in range(0, len(texts), effective_batch_size):
        chunk = texts[i : i + effective_batch_size]

        request = translate.TranslateTextRequest(
            contents=chunk,
            target_language_code=target_lang,
            parent=parent,
            model=model_path,
        )

        if source_lang != "auto":
            request.source_language_code = source_lang

        response = client.translate_text(request=request)

        for idx, translation in enumerate(response.translations):
            translated_text = validate_translation_response(
                translation.translated_text
            )
            if translated_text is None:
                translated_text = chunk[idx]

            detected_source = None
            if translation.detected_language_code:
                detected_source = translation.detected_language_code

            result = TranslationResult(
                translated_text=translated_text,
                source_language=source_lang,
                target_language=target_lang,
                model=model,
                confidence=0.9,
                detected_source_language=detected_source,
            )
            all_results.append(result)

    return BatchTranslationResult(
        results=all_results,
        source_texts=texts,
        target_language=target_lang,
        total_count=len(all_results),
    )


if __name__ == "__main__":
    texts_to_translate = [
        "Hello, world!",
        "How are you today?",
        "Good morning and welcome.",
    ]
    batch_result = batch_translate(texts_to_translate, target_language="ja")
    for src, res in zip(batch_result.source_texts, batch_result.results):
        print(f"  {src} => {res.translated_text}")
