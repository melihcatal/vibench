from google.cloud import translate_v3


def invoice_note_translate(payload, config=None):
    config = config or {}
    client = translate_v3.TranslationServiceClient()
    parent = client.location_path(config['project_id'], config.get('location', 'global'))
    response = client.translate_text(contents=[payload['text']], target_language_code=config['target_language_code'], parent=parent)
    return {'translations': [item.translated_text for item in response.translations]}
