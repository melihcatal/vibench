from google.cloud import translate_v3

from translation_client import get_translation_client, get_translation_parent, get_text_mime_type
from translation_models import normalize_payload


def translate_markup(payload, config=None):
    config = config or {}
    payload = normalize_payload(payload)
    client = get_translation_client()
    parent = get_translation_parent(config)
    response = client.translate_text(request={
        "parent": parent,
        "contents": [payload["html"]],
        "mime_type": get_text_mime_type(True),
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    return {
        "html": response.translations[0].translated_text,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
