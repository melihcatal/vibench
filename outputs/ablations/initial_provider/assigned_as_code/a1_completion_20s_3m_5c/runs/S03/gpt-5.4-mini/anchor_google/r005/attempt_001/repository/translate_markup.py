from google.cloud import translate_v3

from translation_client import get_translation_client, get_translation_parent
from translation_models import normalize_translation_result


def translate_markup(payload, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = get_translation_parent(config)
    response = client.translate_text(request={
        "parent": parent,
        "contents": [payload["markup"]],
        "mime_type": payload.get("mime_type", "text/html"),
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    return normalize_translation_result(response.translations[0], payload["source_language"], payload["target_language"])
