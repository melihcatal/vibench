import os
from google.cloud import translate_v2 as translate


def translate_dictionary_values(
    data_dict: dict, target_language: str = "es", source_language: str = "en"
) -> dict:
    """Translate dictionary values while preserving keys using Google Cloud Translation API."""
    client = translate.Client()

    texts_to_translate = list(data_dict.values())

    results = client.translate(
        texts_to_translate,
        target_language=target_language,
        source_language=source_language,
    )

    translated_dict = {}
    for (key, original_value), result in zip(data_dict.items(), results):
        translated_dict[key] = result["translatedText"]

    return translated_dict
