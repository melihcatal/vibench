import os
from google.cloud import translate_v2 as translate

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'

translate_client = translate.Client()

def translate_dictionary_values(dictionary, target_language):
    translated_dict = {}
    for key, value in dictionary.items():
        result = translate_client.translate(value, target_language=target_language)
        translated_dict[key] = result['translatedText']
    return translated_dict