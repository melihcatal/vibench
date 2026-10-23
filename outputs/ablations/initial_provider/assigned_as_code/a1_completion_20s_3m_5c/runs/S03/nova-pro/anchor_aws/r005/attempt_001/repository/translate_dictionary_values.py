import boto3

from translation_client import get_translation_client


def translate_dictionary_values(dictionary, source_language, target_language, config=None):
    client = get_translation_client(config)
    translated_dict = {}
    for key, value in dictionary.items():
        response = client.translate_text(
            Text=value,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )
        translated_dict[key] = response["TranslatedText"]
    return {
        "dictionary": translated_dict,
        "source_language": source_language,
        "target_language": target_language,
    }
