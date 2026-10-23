import boto3

from translation_models import normalize_language_code, normalize_text_mapping


def translate_dictionary_values(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    values = normalize_text_mapping(payload["values"])
    translated = {}
    for key, value in values.items():
        response = client.translate_text(
            Text=value,
            SourceLanguageCode=normalize_language_code(payload["source_language"]),
            TargetLanguageCode=normalize_language_code(payload["target_language"]),
        )
        translated[key] = response["TranslatedText"]
    return {
        "values": translated,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
