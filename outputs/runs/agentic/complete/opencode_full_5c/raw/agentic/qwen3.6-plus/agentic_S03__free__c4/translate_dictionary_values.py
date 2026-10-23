from typing import Optional

from translation_client import translate_single_text
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResult,
    parse_google_translate_response,
)


def translate_dictionary_values(
    dictionary: dict[str, str],
    target_language: str,
    source_language: Optional[str] = None,
    model: str = "nmt",
    api_key: Optional[str] = None,
) -> DictionaryTranslationResult:
    request = DictionaryTranslationRequest(
        dictionary=dictionary,
        source_language=source_language,
        target_language=target_language,
        model=model,
    )

    translated_dict: dict[str, str] = {}

    for key, value in request.dictionary.items():
        response_data = translate_single_text(
            text=value,
            target_language=request.target_language,
            source_language=request.source_language,
            format_type="text",
            model=request.model,
            api_key=api_key,
        )

        result = parse_google_translate_response(response_data, value)
        translated_dict[key] = result.translated_text

    return DictionaryTranslationResult(translated_dictionary=translated_dict)


def translate_dictionary_with_config(
    config: DictionaryTranslationRequest,
    api_key: Optional[str] = None,
) -> DictionaryTranslationResult:
    return translate_dictionary_values(
        dictionary=config.dictionary,
        target_language=config.target_language,
        source_language=config.source_language,
        model=config.model,
        api_key=api_key,
    )
