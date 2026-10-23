from __future__ import annotations

from translation_client import GOOGLE_TRANSLATE_PROVIDER, detect_mime_type, get_google_translate_client
from translation_models import TranslationRequest, TranslationResult


def translate_markup(request: TranslationRequest) -> TranslationResult:
    client = get_google_translate_client()
    mime_type = detect_mime_type(request.text)
    response = client.translate(
        request.text,
        source_language=request.source_language,
        target_language=request.target_language,
        format_="html" if mime_type == "text/html" else "text",
    )
    return TranslationResult(
        text=response["translatedText"],
        detected_source_language=response.get("detectedSourceLanguage"),
        provider=GOOGLE_TRANSLATE_PROVIDER,
        model="google-cloud-translate-v2",
    )
