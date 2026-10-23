from google.cloud import translate_v3

from translation_client import get_translation_client


def translate_markup(markup, source_language, target_language, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    response = client.translate_text(request={
        "parent": parent,
        "contents": [markup],
        "mime_type": "text/html",
        "source_language_code": source_language,
        "target_language_code": target_language,
   })
    translated_markup = response.translations[0].translated_text
    return translated_markup