from google.cloud import translate_v2 as translate
import os


def translate_dictionary_values(
    data: dict, target_language: str, source_language: str = None
) -> dict:
    client = translate.Client()
    translated_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            result = client.translate(
                value, target_language=target_language, source_language=source_language
            )
            translated_data[key] = result["translatedText"]
        else:
            translated_data[key] = value
    return translated_data
