from translation_client import (
    build_translation_client,
    detect_target_formality,
    extract_translated_text,
)
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(source_language: str, target_language: str, text, **options):
    request = TranslationRequest(
        source_language=source_language,
        target_language=target_language,
        text=text,
        options=options,
    )
    client = build_translation_client()
    translated = client.translate_text(
        normalize_text(request.text),
        source_lang=request.source_language,
        target_lang=request.target_language,
        formality=detect_target_formality(request.options),
    )
    return TranslationResponse(
        source_language=request.source_language,
        target_language=request.target_language,
        translated=extract_translated_text(translated),
        provider="DeepL API",
        raw=translated,
    )
