import boto3

def translate_dictionary_values(dictionary: dict, source_language: str, target_language: str) -> dict:
    """
    Translates dictionary values while preserving keys using AWS Translate.
    """
    client = boto3.client("translate")
    translated_dictionary = {}
    for key, value in dictionary.items():
        if isinstance(value, str):
            response = client.translate_text(
                Text=value,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language
            )
            translated_dictionary[key] = response["TranslatedText"]
        else:
            translated_dictionary[key] = value
    return translated_dictionary
