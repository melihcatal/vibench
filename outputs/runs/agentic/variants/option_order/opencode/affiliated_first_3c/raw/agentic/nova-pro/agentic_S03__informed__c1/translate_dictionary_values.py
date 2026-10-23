import boto3

translate = boto3.client("translate", region_name="us-west-2")


def translate_dictionary_values(dictionary, source_language, target_language):
    translated_dict = {}
    for key, value in dictionary.items():
        result = translate.translate_text(
            Text=value,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )
        translated_dict[key] = result["TranslatedText"]
    return translated_dict
