from google.cloud import translate_v3

from translation_client import get_client, get_config
from translation_models import normalize_payload, normalize_response


def translate_markup(markup, source_language, target_language):
    config = get_config()
    client = get_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    payload = {
        'contents': [markup],
        'mime_type': 'text/html',
        'source_language_code': source_language,
        'target_language_code': target_language,
    }
    normalized_payload = normalize_payload(payload)
    response = client.translate_text(request=normalized_payload)
    translated_markup = response.translations[0].translated_text
    return translated_markup