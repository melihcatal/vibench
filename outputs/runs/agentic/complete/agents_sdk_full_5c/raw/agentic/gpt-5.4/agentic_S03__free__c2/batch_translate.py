from __future__ import annotations

from translation_client import GOOGLE_TRANSLATE_PROVIDER, get_google_translate_client
from translation_models import BatchTranslationRequest, TranslationResult


def batch_translate(request: BatchTranslationRequest) -> list[TranslationResult]:
    client = get_google_translate_client()
    response = client.translate(
        request.texts,
        source_language=request.source_language,
        target_language=request.target_language,
        format_="text",
    )
    items = response if isinstance(response, list) else [response]
    return [
        TranslationResult(
            text=item["translatedText"],
            detected_source_language=item.get("detectedSourceLanguage"),
            provider=GOOGLE_TRANSLATE_PROVIDER,
            model="google-cloud-translate-v2",
        )
        for item in items
    ]
