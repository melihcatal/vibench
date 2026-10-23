import os
from google.cloud import translate_v2 as translate


def translate_dictionary_values(input_dict, target_language="en", source_language=None):
    """Translate dictionary values while preserving keys using Google Cloud Translation."""
    client = translate.Client()

    values = list(input_dict.values())

    kwargs = {"target_language": target_language, "values": values}
    if source_language:
        kwargs["source_language"] = source_language

    results = client.translate(**kwargs)

    translated_dict = {}
    keys = list(input_dict.keys())

    for i, (key, original_value) in enumerate(input_dict.items()):
        translated_dict[key] = {
            "original": original_value,
            "translated": results[i]["translatedText"],
            "source_language": results[i].get(
                "detectedSourceLanguage", source_language
            ),
            "target_language": target_language,
        }

    return translated_dict
