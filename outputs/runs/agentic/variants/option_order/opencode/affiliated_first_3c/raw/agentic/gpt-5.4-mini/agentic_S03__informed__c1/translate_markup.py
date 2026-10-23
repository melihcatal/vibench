from translation_client import build_translation_client, extract_translated_text
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_markup(source_language: str, target_language: str, markup, **options):
    request = TranslationRequest(
        source_language=source_language,
        target_language=target_language,
        text=markup,
        format="html",
        options=options,
    )
    client = build_translation_client()
    translated = client.translate_text(
        normalize_text(request.text),
        source_lang=request.source_language,
        target_lang=request.target_language,
        tag_handling="html",
    )
    return TranslationResponse(
        source_language=request.source_language,
        target_language=request.target_language,
        translated=extract_translated_text(translated),
        provider="DeepL API",
        raw=translated,
    )
