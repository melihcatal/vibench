from google.cloud import translate_v3

from translation_client import get_translation_client, get_translation_parent
from translation_models import normalize_payload


def quality_summary(payload, config=None):
    config = config or {}
    payload = normalize_payload(payload)
    client = get_translation_client()
    parent = get_translation_parent(config)
    response = client.translate_text(request={
        "parent": parent,
        "contents": [payload["text"]],
        "mime_type": "text/plain",
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    translated_text = response.translations[0].translated_text
    return {
        "issues": [] if translated_text else ["empty_translation"],
        "translated_text": translated_text,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
