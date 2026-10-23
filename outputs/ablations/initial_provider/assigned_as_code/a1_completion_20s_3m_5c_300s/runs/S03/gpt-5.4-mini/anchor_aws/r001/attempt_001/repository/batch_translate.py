from translation_client import get_translation_client, translate_with_client
from translation_models import normalize_payload


def batch_translate(payload, config=None):
    payload = normalize_payload(payload)
    client = get_translation_client(config)
    translated = [
        translate_with_client(client, text, payload["source_language"], payload["target_language"])
        for text in payload["texts"]
    ]
    return {
        "texts": translated,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
