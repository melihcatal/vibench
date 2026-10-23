from google.cloud import translate_v3 as translate

from document_models import normalize_text


def ocr_translate(payload, config=None):
    payload = payload or {}
    config = config or {}
    text = normalize_text(payload.get('text'))
    client = translate.TranslationServiceClient()
    parent = client.location_path(config.get('project_id'), config.get('location', 'global'))
    response = client.translate_text(contents=[text], target_language_code=config.get('target_language', 'en'), parent=parent, mime_type='text/plain')
    translated = response.translations[0].translated_text if response.translations else ''
    return {'translated_text': translated}
