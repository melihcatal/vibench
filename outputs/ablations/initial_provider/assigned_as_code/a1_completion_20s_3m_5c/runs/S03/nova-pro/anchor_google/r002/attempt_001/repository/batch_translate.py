from google.cloud import translate_v3

from translation_client import get_translation_client


def batch_translate(texts, source_language, target_language, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    response = client.batch_translate_text(request={
        "parent": parent,
        "source_language_code": source_language,
        "target_language_code": target_language,
        "mime_type": "text/plain",
        "contents": texts,
   })
    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)
    return translations