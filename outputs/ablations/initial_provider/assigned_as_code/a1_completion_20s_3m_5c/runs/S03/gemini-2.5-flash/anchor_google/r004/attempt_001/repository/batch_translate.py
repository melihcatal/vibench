from google.cloud import translate_v3


def batch_translate(payload, config=None):
    config = config or {}
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    response = client.translate_text(request={
        "parent": parent,
        "contents": payload["texts"],
        "mime_type": "text/plain",
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    return {
        "translated_texts": [translation.translated_text for translation in response.translations],
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
