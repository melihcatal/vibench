from translation_client import get_translate_client
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
)
from google.cloud.translate_v3.types import TranslateTextRequest


def translate_dictionary_values(
    dictionary: dict[str, str], target_language: str, source_language: str = None
) -> dict[str, str]:
    client = get_translate_client()
    parent = f"projects/{client.project_id}"

    # Extract values to translate
    values_to_translate = list(dictionary.values())
    keys = list(dictionary.keys())

    if not values_to_translate:
        return {}

    request = TranslateTextRequest(
        parent=parent,
        contents=values_to_translate,
        target_language_code=target_language,
        source_language_code=source_language if source_language else None,
        mime_type="text/plain",
    )
    response = client.translate_text(request=request)

    translated_values = [
        translation.translated_text for translation in response.translations
    ]
    translated_dictionary = {keys[i]: translated_values[i] for i in range(len(keys))}

    return DictionaryTranslationResponse(translated_dictionary).to_dict()
