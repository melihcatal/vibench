from google.cloud import translate_v3

from translation_client import get_translation_client


def quality_summary(payload, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    response = client.translate_text(request={
        "parent": parent,
        "contents": [payload['text']],
        "mime_type": "text/plain",
        "source_language_code": payload['source_language'],
        "target_language_code": payload['target_language'],
    }
    )
    translation = response.translations[0]
    return {
        'text': translation.translated_text,
        'source_language': payload['source_language'],
        'target_language': payload['target_language'],
        'quality_issues': translation.detected_language_code!= payload['source_language']
    }

