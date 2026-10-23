from typing import Dict

from translation_client import translate_dict_values
from translation_models import TranslationRequest, TranslationResponse


def translate_dictionary_values(
    request: TranslationRequest, values: Dict[str, str]
) -> TranslationResponse:
    translated = translate_dict_values(
        values, request.target_language, request.source_language
    )
    return TranslationResponse(
        translated_text=str(translated),
        source_language=request.source_language,
        target_language=request.target_language,
    )
