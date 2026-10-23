from __future__ import annotations

from google.cloud import translate_v2 as translate

from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse


def translate_stored_text(
    request: StoredTextTranslateRequest,
) -> StoredTextTranslateResponse:
    client = translate.Client()
    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
        format_="text",
    )
    return StoredTextTranslateResponse(
        provider="google_cloud_translate",
        translated_text=result["translatedText"],
        detected_source_language=result.get("detectedSourceLanguage"),
        target_language=request.target_language,
    )
