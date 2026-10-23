from google.cloud import translate_v2 as translate
from translation_client import translate_client

def translate_dictionary_values(dictionary, target_language):
    client = translate_client()
    translated_dict = {}
    for key, value in dictionary.items():
        result = client.translate(value, target_language=target_language)
        translated_dict[key] = result['translatedText']
    return translated_dict