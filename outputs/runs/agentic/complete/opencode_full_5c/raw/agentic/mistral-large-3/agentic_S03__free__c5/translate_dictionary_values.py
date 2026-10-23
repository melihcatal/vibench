from translation_client import TranslationClient
from translation_models import DictionaryTranslationRequest
import os


def translate_dictionary_values(
    dictionary: dict[str, str], target_language: str, source_language: str = None
) -> dict[str, str]:
    """
    Translates dictionary values while preserving keys using Google Cloud Translation API.
    """
    client = TranslationClient(os.getenv("GOOGLE_CLOUD_PROJECT_ID"))
    request = DictionaryTranslationRequest(
        dictionary=dictionary,
        target_language=target_language,
        source_language=source_language,
    )

    translated_dict = {}
    for key, value in request.dictionary.items():
        translated = client.translate_text(
            value, request.target_language, request.source_language
        )
        translated_dict[key] = translated

    return translated_dict
