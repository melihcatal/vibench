from google.cloud import translate_v3

from translation_client import get_translation_client, get_translation_parent
from translation_models import normalize_translation_result


def batch_translate(payload, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = get_translation_parent(config)
    response = client.translate_text(request={
        "parent": parent,
        "contents": payload["texts"],
        "mime_type": "text/plain",
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    return {
        "translations": [
            normalize_translation_result(item, payload["source_language"], payload["target_language"])
            for item in response.translations
        ]
    }
