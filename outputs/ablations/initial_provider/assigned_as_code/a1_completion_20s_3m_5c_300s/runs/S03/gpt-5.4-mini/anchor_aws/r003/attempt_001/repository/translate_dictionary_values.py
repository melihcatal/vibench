from translation_client import get_translate_client
from translation_models import normalize_dictionary_payload


def translate_dictionary_values(payload, config=None):
    payload = normalize_dictionary_payload(payload)
    client = get_translate_client(config)
    translated = {}
    for key, value in payload["values"].items():
        response = client.translate_text(
            Text=str(value),
            SourceLanguageCode=payload["source_language"],
            TargetLanguageCode=payload["target_language"],
        )
        translated[key] = response["TranslatedText"]
    return {
        "values": translated,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
