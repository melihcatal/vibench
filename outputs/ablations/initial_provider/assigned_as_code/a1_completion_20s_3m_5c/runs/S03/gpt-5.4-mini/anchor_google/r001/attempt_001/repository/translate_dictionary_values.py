from google.cloud import translate_v3

from translation_client import get_translation_client, get_translation_parent
from translation_models import normalize_payload


def translate_dictionary_values(payload, config=None):
    config = config or {}
    payload = normalize_payload(payload)
    client = get_translation_client()
    parent = get_translation_parent(config)
    keys = list(payload["values"].keys())
    contents = [str(payload["values"][key]) for key in keys]
    response = client.translate_text(request={
        "parent": parent,
        "contents": contents,
        "mime_type": "text/plain",
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    return {
        "values": {key: response.translations[index].translated_text for index, key in enumerate(keys)},
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
