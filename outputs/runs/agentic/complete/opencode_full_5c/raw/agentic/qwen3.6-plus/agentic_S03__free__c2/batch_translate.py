from typing import List
from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResponse,
    TranslationResponse,
    normalize_language_code,
    normalize_response_text,
    calculate_character_count,
)
from translation_client import (
    get_deepl_client,
    build_translation_options,
    DEEPL_API_ENDPOINT,
)


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client = get_deepl_client()
    source_lang = normalize_language_code(request.source_lang)
    target_lang = normalize_language_code(request.target_lang)
    options = build_translation_options(
        source_lang=source_lang,
        target_lang=target_lang,
        preserve_formatting=True,
    )
    results = client.translate_text(request.texts, **options)
    translations = []
    for i, result in enumerate(results):
        translations.append(
            TranslationResponse(
                translated_text=normalize_response_text(result.text),
                source_lang=result.source_lang,
                target_lang=target_lang,
                character_count=len(request.texts[i]),
            )
        )
    return BatchTranslationResponse(
        translations=translations,
        total_characters=calculate_character_count(request.texts),
    )
