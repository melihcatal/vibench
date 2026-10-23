import os
from google.cloud import translate_v2 as translate


def translate_dictionary_values(
    data_dict: dict, target_language: str = "es", source_language: str = "en"
) -> dict:
    """
    Translate dictionary values while preserving keys using Google Cloud Translation.

    Args:
        data_dict: Dictionary with string values to translate
        target_language: Target language code (default: "es" for Spanish)
        source_language: Source language code (default: "en" for English)

    Returns:
        Dictionary with same keys and translated values
    """
    client = translate.Client()

    texts_to_translate = list(data_dict.values())

    results = client.translate(
        texts_to_translate,
        target_language=target_language,
        source_language=source_language,
    )

    translated_values = [result["translatedText"] for result in results]

    translated_dict = {}
    for i, (key, _) in enumerate(data_dict.items()):
        translated_dict[key] = translated_values[i]

    return translated_dict
