from google.cloud import translate_v3

from translation_client import get_translation_client


def translate_dictionary_values(payload, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    translated_values = {}
    for key, value in payload['dictionary'].items():
        response = client.translate_text(request={
            "parent": parent,
            "contents": [value],
            "mime_type": "text/plain",
            "source_language_code": payload['source_language'],
            "target_language_code": payload['target_language'],
        }
        )
        translated_values[key] = response.translations[0].translated_text
    return {
        "dictionary": translated_values,
        "source_language": payload['source_language'],
        "target_language": payload['target_language'],
    }

