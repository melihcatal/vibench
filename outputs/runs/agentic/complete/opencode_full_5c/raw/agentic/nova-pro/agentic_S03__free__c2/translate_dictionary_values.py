import boto3

translate = boto3.client("translate", region_name="us-west-2")


def translate_dictionary_values(dictionary, source_lang, target_lang):
    translated_dict = {}
    for key, value in dictionary.items():
        translated_value = translate.translate_text(
            Text=value, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
        )
        translated_dict[key] = translated_value.translation_text
    return translated_dict
