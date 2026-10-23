from translation_client import build_translation_client, extract_translated_text
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    normalize_text_list,
)


def batch_translate(source_language: str, target_language: str, texts, **options):
    request = TranslationRequest(
        source_language=source_language,
        target_language=target_language,
        text=texts,
        options=options,
    )
    client = build_translation_client()
    payload = normalize_text_list(request.text)
    results = client.translate_text(
        payload,
        source_lang=request.source_language,
        target_lang=request.target_language,
    )
    translated = [extract_translated_text(item) for item in results]
    return TranslationResponse(
        source_language=request.source_language,
        target_language=request.target_language,
        translated=translated,
        provider="DeepL API",
        raw=results,
    )
