from google.cloud import translate_v3

from translation_client import build_translation_parent, load_translation_config
from translation_models import normalize_payload


def batch_translate(payload, config=None):
    config = load_translation_config(config)
    client = translate_v3.TranslationServiceClient()
    parent = build_translation_parent(config)
    items = [normalize_payload(item) for item in payload["items"]]
    response = client.translate_text(request={
        "parent": parent,
        "contents": [item["text"] for item in items],
        "mime_type": "text/plain",
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    return {
        "items": [translation.translated_text for translation in response.translations],
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
