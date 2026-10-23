from google.cloud import translate_v3

from translation_client import get_config, get_translation_client
from translation_models import batch_translate_payload, batch_translate_result


def batch_translate(payload, config=None):
    config = get_config(config)
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    items = batch_translate_payload(payload)
    response = client.translate_text(request={
        "parent": parent,
        "contents": [item["text"] for item in items],
        "mime_type": "text/plain",
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    return batch_translate_result(response.translations, items, payload)
