from google.cloud import translate_v3

from translation_client import load_translation_config, build_parent
from translation_models import normalize_mapping_values


def translate_dictionary_values(payload, config=None):
    config = load_translation_config(config)
    client = translate_v3.TranslationServiceClient()
    keys = list(payload["values"].keys())
    values = normalize_mapping_values(payload["values"])
    response = client.translate_text(request={
        "parent": build_parent(config),
        "contents": list(values.values()),
        "mime_type": "text/plain",
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    translated = {key: item.translated_text for key, item in zip(keys, response.translations)}
    return {
        "values": translated,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
