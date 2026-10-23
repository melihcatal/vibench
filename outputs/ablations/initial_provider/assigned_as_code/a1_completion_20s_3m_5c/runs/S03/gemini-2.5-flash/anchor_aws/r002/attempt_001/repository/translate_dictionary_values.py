import boto3
from translation_client import get_translate_client
from translation_models import parse_translation_response


def translate_dictionary_values(payload, config=None):
    config = config or {}
    client = get_translate_client(region_name=config.get("region"))

    translated_dict = {}
    source_language = payload["source_language"]
    target_language = payload["target_language"]

    for key, value in payload["data"].items():
        if isinstance(value, str):
            response = client.translate_text(
                Text=value,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language,
            )
            translated_dict[key] = response["TranslatedText"]
        else:
            translated_dict[key] = value

    return {
        "data": translated_dict,
        "source_language": source_language,
        "target_language": target_language,
    }
