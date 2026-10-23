from translation_client import google_translate_client
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
)


def translate_dictionary_values(
    request: DictionaryTranslationRequest,
) -> DictionaryTranslationResponse:
    """
    Translates dictionary values.
    """
    if not request.source_dictionary:
        return DictionaryTranslationResponse(translated_dictionary={})

    keys = list(request.source_dictionary.keys())
    values = list(request.source_dictionary.values())

    translated_values_result = google_translate_client.translate(
        values, target_language=request.target_lang, source_language=request.source_lang
    )

    translated_values = [item["translatedText"] for item in translated_values_result]

    translated_dictionary = dict(zip(keys, translated_values))

    detected_source_lang = ""
    if translated_values_result:
        detected_source_lang = translated_values_result[0].get(
            "detectedSourceLanguage", ""
        )

    return DictionaryTranslationResponse(
        translated_dictionary=translated_dictionary,
        detected_source_lang=detected_source_lang,
    )
