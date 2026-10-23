import boto3

from translation_client import get_translate_client
from translation_models import TranslationRequest, TranslationResponse


def translate_dictionary_values(dictionary, source_language, target_language, config=None):
    client = get_translate_client(config)
    translated_dict = {}
    for key, value in dictionary.items():
        request = TranslationRequest(text=value, source_language=source_language, target_language=target_language).to_dict()
        response = client.translate_text(**request)
        translated_dict[key] = TranslationResponse.from_dict(response).to_dict()['text']
    return translated_dict