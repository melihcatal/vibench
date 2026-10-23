from google.cloud import translate_v3

from translation_client import get_client, get_config
from translation_models import normalize_payload, normalize_response


def embed_translation_memory(text, source_language, target_language):
    config = get_config()
    client = get_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    payload = {
        'contents': [text],
        'mime_type': 'text/plain',
        'source_language_code': source_language,
        'target_language_code': target_language,
    }
    normalized_payload = normalize_payload(payload)
    response = client.translate_text(request=normalized_payload)
    translated_text = response.translations[0].translated_text
    # Placeholder for actual translation memory embedding logic
    return f"Translation memory embedding for '{text}' translated to '{target_language}': [placeholder]"