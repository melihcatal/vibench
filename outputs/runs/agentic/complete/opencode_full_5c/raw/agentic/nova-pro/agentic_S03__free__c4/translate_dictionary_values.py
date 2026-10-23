import boto3


def translate_dictionary_values(dictionary, source_lang, target_lang):
    client = boto3.client("translate")
    translated_dict = {}
    for key, value in dictionary.items():
        translated_value = translate_text(value, source_lang, target_lang)
        translated_dict[key] = translated_value
    return translated_dict
