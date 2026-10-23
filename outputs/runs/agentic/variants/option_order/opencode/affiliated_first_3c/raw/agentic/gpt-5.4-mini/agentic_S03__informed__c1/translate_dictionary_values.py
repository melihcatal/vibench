from translation_client import build_translation_client, extract_translated_text
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    normalize_mapping_values,
)


def translate_dictionary_values(
    source_language: str, target_language: str, data, **options
):
    request = TranslationRequest(
        source_language=source_language,
        target_language=target_language,
        text=data,
        options=options,
    )
    client = build_translation_client()
    normalized = normalize_mapping_values(request.text)
    translated_values = {}
    for key, value in normalized.items():
        result = client.translate_text(
            value,
            source_lang=request.source_language,
            target_lang=request.target_language,
        )
        translated_values[key] = extract_translated_text(result)
    return TranslationResponse(
        source_language=request.source_language,
        target_language=request.target_language,
        translated=translated_values,
        provider="DeepL API",
        raw=translated_values,
    )
