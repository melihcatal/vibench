import os
from google.cloud import translate_v2 as translate

def translate_dictionary_values(dictionary, target_language):
    client = translate.Client()
    translated_dict = {}
    for key, value in dictionary.items():
        translated_dict[key] = client.translate(value, target_language=target_language)['translatedText']
    return translated_dict