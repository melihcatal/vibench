import boto3

from translation_client import get_translate_client
from translation_models import normalize_translation_payload, normalize_translation_response


def translate_dictionary_values(dictionary, source_language, target_language, config=None):
    client = get_translate_client(config)
    translated_dict = {}
    for key, value in dictionary.items():
        payload = normalize_translation_payload(
            text=value,
            source_language=source_language,
            target_language=target_language,
        )
        response = client.translate_text(**payload)
        translated_text = response["TranslatedText"]
        translated_dict[key] = normalize_translation_response(response)
    return translated_dict