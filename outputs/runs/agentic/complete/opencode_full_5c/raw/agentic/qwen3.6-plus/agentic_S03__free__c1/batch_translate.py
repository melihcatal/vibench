import os
from typing import List, Optional
from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResponse,
    TranslationResponse,
    normalize_language_code,
    normalize_text,
)
from translation_client import (
    GoogleTranslationClient,
    GOOGLE_TRANSLATE_API_KEY,
    GOOGLE_TRANSLATE_API_ENDPOINT,
    DEFAULT_GOOGLE_MODEL,
    create_translation_client,
)


def batch_translate(
    texts: List[str],
    source_language: str,
    target_language: str,
    model: str = DEFAULT_GOOGLE_MODEL,
    api_key: Optional[str] = None,
) -> BatchTranslationResponse:
    key = api_key or GOOGLE_TRANSLATE_API_KEY
    client = create_translation_client(api_key=key)
    cleaned_texts = [normalize_text(t) for t in texts]
    request = BatchTranslationRequest(
        texts=cleaned_texts,
        source_language=normalize_language_code(source_language),
        target_language=normalize_language_code(target_language),
        model=model,
        content_type="text",
    )
    return client.batch_translate(request)


def batch_translate_ordered(
    texts: List[str],
    source_language: str,
    target_language: str,
    model: str = DEFAULT_GOOGLE_MODEL,
    api_key: Optional[str] = None,
) -> List[TranslationResponse]:
    response = batch_translate(texts, source_language, target_language, model, api_key)
    ordered_results = [None] * response.total_count
    for i, translation in enumerate(response.translations):
        ordered_results[i] = translation
    for idx in response.failed_indices:
        ordered_results[idx] = TranslationResponse(
            translated_text="",
            source_language=source_language,
            target_language=target_language,
            model_used=model,
        )
    return [r for r in ordered_results if r is not None]


def batch_translate_via_http(
    texts: List[str],
    source_language: str,
    target_language: str,
    model: str = DEFAULT_GOOGLE_MODEL,
    api_key: Optional[str] = None,
) -> BatchTranslationResponse:
    import requests

    key = api_key or os.environ.get("GOOGLE_TRANSLATE_API_KEY", "")
    endpoint = GOOGLE_TRANSLATE_API_ENDPOINT
    payload = {
        "q": [normalize_text(t) for t in texts],
        "source": normalize_language_code(source_language),
        "target": normalize_language_code(target_language),
        "format": "text",
        "model": model,
    }
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": key,
    }
    response = requests.post(endpoint, json=payload, headers=headers)
    response.raise_for_status()
    api_response = response.json()
    data = api_response.get("data", {})
    translations = data.get("translations", [])
    results = []
    failed_indices = []
    for i, text in enumerate(texts):
        if i < len(translations):
            translation = translations[i]
            results.append(
                TranslationResponse(
                    translated_text=translation.get("translatedText", ""),
                    source_language=source_language,
                    target_language=normalize_language_code(target_language),
                    model_used=model,
                    detected_source_language=translation.get("detectedSourceLanguage"),
                )
            )
        else:
            failed_indices.append(i)
    return BatchTranslationResponse(
        translations=results,
        total_count=len(texts),
        successful_count=len(results),
        failed_indices=failed_indices,
    )
