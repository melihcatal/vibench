from google.cloud import translate_v2 as translate


def translate_dictionary_values(dictionary, target_language):
    client = translate.Client()
    translated_dict = {}
    for key, value in dictionary.items():
        translated_value = client.translate(value, target_language=target_language)[
            "translatedText"
        ]
        translated_dict[key] = translated_value
    return translated_dict
