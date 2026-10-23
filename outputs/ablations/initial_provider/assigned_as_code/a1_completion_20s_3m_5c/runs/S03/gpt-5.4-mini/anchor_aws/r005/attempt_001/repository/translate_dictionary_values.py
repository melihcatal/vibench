from translation_client import translation_client
from translation_models import normalize_dictionary_values, normalize_language_code


def translate_dictionary_values(payload, config=None):
    config = config or {}
    client = translation_client(config)
    values = normalize_dictionary_values(payload.get("values"))
    translated = {}
    for key, value in values.items():
        translated[key] = client.translate_text(
            Text=value,
            SourceLanguageCode=normalize_language_code(payload.get("source_language")),
            TargetLanguageCode=normalize_language_code(payload.get("target_language")),
        )["TranslatedText"]
    return {
        "values": translated,
        "source_language": payload.get("source_language"),
        "target_language": payload.get("target_language"),
    }
