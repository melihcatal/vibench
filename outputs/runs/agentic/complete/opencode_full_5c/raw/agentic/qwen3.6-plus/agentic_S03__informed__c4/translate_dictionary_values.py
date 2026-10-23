from translation_client import translate_dictionary_values
from translation_models import DictionaryTranslationRequest


def translate_dictionary_values(
    data: dict[str, str],
    source_language: str,
    target_language: str,
    formality: str | None = None,
) -> dict[str, str]:
    request = DictionaryTranslationRequest(
        data=data,
        source_language=source_language,
        target_language=target_language,
        formality=formality,
    )
    result = translate_dictionary_values(
        data=request.data,
        source_language=request.source_language,
        target_language=request.target_language,
        formality=request.formality,
    )
    return result
