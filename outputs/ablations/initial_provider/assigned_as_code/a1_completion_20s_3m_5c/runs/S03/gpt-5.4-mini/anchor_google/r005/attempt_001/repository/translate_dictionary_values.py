from google.cloud import translate_v3

from translation_client import get_translation_client, get_translation_parent
from translation_models import normalize_translation_result


def translate_dictionary_values(payload, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = get_translation_parent(config)
    keys = list(payload["data"].keys())
    response = client.translate_text(request={
        "parent": parent,
        "contents": [str(payload["data"][key]) for key in keys],
        "mime_type": "text/plain",
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    return {
        key: normalize_translation_result(item, payload["source_language"], payload["target_language"])["text"]
        for key, item in zip(keys, response.translations)
    }
