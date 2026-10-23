from google.cloud import translate_v3

from translation_client import get_translation_client


def batch_translate(payloads, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    requests = [
        {
            "contents": [payload['text']],
            "mime_type": "text/plain",
            "source_language_code": payload['source_language'],
            "target_language_code": payload['target_language'],
        }
        for payload in payloads
    ]
    response = client.batch_translate_text(requests=requests, parent=parent)
    translations = [
        {
            "text": translation.translations[0].translated_text,
            "source_language": payload['source_language'],
            "target_language": payload['target_language'],
        }
        for translation, payload in zip(response.translations, payloads)
    ]
    return translations