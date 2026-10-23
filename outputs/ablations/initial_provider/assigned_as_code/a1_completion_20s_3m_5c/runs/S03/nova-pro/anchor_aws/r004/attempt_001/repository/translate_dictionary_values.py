import boto3


def translate_dictionary_values(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    dictionary = payload["dictionary"]
    source_language = payload["source_language"]
    target_language = payload["target_language"]
    translated_dictionary = {}
    for key, value in dictionary.items():
        response = client.translate_text(
            Text=value,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )
        translated_dictionary[key] = response["TranslatedText"]
    return {
        "dictionary": translated_dictionary,
        "source_language": source_language,
        "target_language": target_language,
    }