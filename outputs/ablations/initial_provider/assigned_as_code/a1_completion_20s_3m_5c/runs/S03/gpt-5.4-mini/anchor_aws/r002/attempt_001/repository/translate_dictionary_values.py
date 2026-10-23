import boto3

from translation_models import normalize_dictionary_payload


def translate_dictionary_values(payload, config=None):
    request = normalize_dictionary_payload(payload)
    client = boto3.client("translate", region_name=(config or {}).get("region"))
    translated = {}
    for key, value in request["values"].items():
        response = client.translate_text(
            Text=value,
            SourceLanguageCode=request["source_language"],
            TargetLanguageCode=request["target_language"],
        )
        translated[key] = response["TranslatedText"]
    return {
        "values": translated,
        "source_language": request["source_language"],
        "target_language": request["target_language"],
    }
