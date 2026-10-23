from translation_client import deepl_translator
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
)


def translate_dictionary_values(
    request: DictionaryTranslationRequest,
) -> DictionaryTranslationResponse:
    if not deepl_translator:
        raise ValueError(
            "DeepL translator not initialized. Please set DEEPL_AUTH_KEY environment variable."
        )

    translated_data = {}
    detected_source_lang = None
    for key, value in request.data.items():
        result = deepl_translator.translate_text(
            value, target_lang=request.target_lang, source_lang=request.source_lang
        )
        translated_data[key] = result.text
        if not detected_source_lang:  # Capture the first detected source language
            detected_source_lang = result.detected_source_lang

    return DictionaryTranslationResponse(
        translated_data=translated_data,
        source_lang=detected_source_lang,
        target_lang=request.target_lang,
    )
