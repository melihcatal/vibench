from google.cloud import translate_v3

from translation_client import get_translation_client, get_translation_parent
from translation_models import normalize_payload


def batch_translate(payload, config=None):
    config = config or {}
    payload = normalize_payload(payload)
    client = get_translation_client()
    parent = get_translation_parent(config)
    response = client.translate_text(request={
        "parent": parent,
        "contents": payload["texts"],
        "mime_type": "text/plain",
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    return {
        "texts": [item.translated_text for item in response.translations],
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
