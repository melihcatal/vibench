from __future__ import annotations

from translation_client import GOOGLE_TRANSLATE_PROVIDER, get_google_translate_client
from translation_models import TranslationRequest, TranslationResult


def translate_text(request: TranslationRequest) -> TranslationResult:
    client = get_google_translate_client()
    response = client.translate(
        request.text,
        source_language=request.source_language,
        target_language=request.target_language,
        format_="text",
    )
    return TranslationResult(
        text=response["translatedText"],
        detected_source_language=response.get("detectedSourceLanguage"),
        provider=GOOGLE_TRANSLATE_PROVIDER,
        model="google-cloud-translate-v2",
    )
