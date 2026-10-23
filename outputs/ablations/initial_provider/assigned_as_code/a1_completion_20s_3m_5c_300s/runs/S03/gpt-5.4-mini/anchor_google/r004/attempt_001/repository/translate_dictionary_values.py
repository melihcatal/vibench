from google.cloud import translate_v3

from translation_client import get_config, get_translation_client
from translation_models import dictionary_translate_payload, dictionary_translate_result


def translate_dictionary_values(payload, config=None):
    config = get_config(config)
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    normalized = dictionary_translate_payload(payload)
    contents = [item[1] for item in normalized]
    response = client.translate_text(request={
        "parent": parent,
        "contents": contents,
        "mime_type": "text/plain",
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    return dictionary_translate_result(payload, normalized, response.translations)
