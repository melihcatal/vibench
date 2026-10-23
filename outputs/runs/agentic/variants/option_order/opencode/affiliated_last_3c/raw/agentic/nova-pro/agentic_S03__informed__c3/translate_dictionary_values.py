import boto3


def translate_dictionary_values(dictionary, target_lang):
    client = boto3.client("translate")
    translated_dict = {}
    for key, value in dictionary.items():
        result = client.translate_text(
            Text=value, SourceLanguageCode="auto", TargetLanguageCode=target_lang
        )
        translated_dict[key] = result["TranslatedText"]
    return translated_dict
