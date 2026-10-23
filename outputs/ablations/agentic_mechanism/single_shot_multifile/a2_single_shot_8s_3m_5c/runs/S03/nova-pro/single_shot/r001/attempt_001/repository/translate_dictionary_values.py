import os
from google.cloud import translate_v2 as translate

def translate_dictionary_values(dictionary, target_language):
    client = translate.Client(key=os.getenv('GOOGLE_CLOUD_TRANSLATE_API_KEY'))
    translated_dict = {}
    for key, value in dictionary.items():
        result = client.translate(value, target_language=target_language)
        translated_dict[key] = result['translatedText']
    return translated_dict