from google.cloud import translate_v2 as translate

def translate_dictionary_values(dictionary, target_language='en'):
    client = translate.Client()
    translated_dict = {}
    for key, value in dictionary.items():
        translation = client.translate(value, target_language=target_language)
        translated_dict[key] = translation['translatedText']
    return translated_dict