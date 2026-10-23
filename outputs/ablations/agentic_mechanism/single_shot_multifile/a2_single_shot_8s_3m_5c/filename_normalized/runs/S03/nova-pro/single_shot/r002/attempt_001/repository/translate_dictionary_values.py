import os
from google.cloud import translate_v2 as translate

def translate_dictionary_values(dictionary, target_language='es'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = translate.Client()
    translated_dict = {}
    for key, value in dictionary.items():
        result = client.translate(value, target_language=target_language)
        translated_dict[key] = result['translatedText']
    return translated_dict