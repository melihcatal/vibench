from google.cloud import translate_v3

from translation_client import get_config, get_translation_client
from translation_models import markup_translate_payload, markup_translate_result


def translate_markup(payload, config=None):
    config = get_config(config)
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    normalized = markup_translate_payload(payload)
    response = client.translate_text(request={
        "parent": parent,
        "contents": [normalized["text"]],
        "mime_type": normalized["mime_type"],
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    return markup_translate_result(response.translations[0].translated_text, payload, normalized)
