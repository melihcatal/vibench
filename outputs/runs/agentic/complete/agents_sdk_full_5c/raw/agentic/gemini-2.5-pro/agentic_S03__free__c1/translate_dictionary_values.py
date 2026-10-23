from typing import Dict
from google.cloud import translate_v2 as translate


def translate_dict_values(
    data: Dict[str, str], source_language: str, target_language: str
) -> Dict[str, str]:
    """
    Translates the string values of a dictionary, preserving keys.
    Provider: Google Cloud Translate API
    """
    if not data:
        return {}
    
    # Instantiates a client. Assumes GOOGLE_APPLICATION_CREDENTIALS is set.
    translation_client = translate.Client()

    keys = list(data.keys())
    values_to_translate = list(data.values())

    # The API call preserves the order of the input list.
    translated_results = translation_client.translate(
        values_to_translate,
        target_language=target_language,
        source_language=source_language
    )

    translated_values = [item['translatedText'] for item in translated_results]

    return dict(zip(keys, translated_values))
