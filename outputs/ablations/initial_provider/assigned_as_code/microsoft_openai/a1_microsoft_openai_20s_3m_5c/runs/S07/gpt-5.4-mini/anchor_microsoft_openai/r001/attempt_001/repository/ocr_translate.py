from google.cloud import translate_v3 as translate

from document_models import normalize_config, normalize_payload, extract_content


def ocr_translate(payload, config=None):
    payload = normalize_payload(payload)
    config = normalize_config(config)
    client = translate.TranslationServiceClient()
    parent = f"projects/{config.get('project_id', 'project')}/locations/{config.get('location', 'global')}"
    response = client.translate_text(
        parent=parent,
        contents=[extract_content(payload)],
        mime_type='text/plain',
        source_language_code=config['source_language'],
        target_language_code=config['target_language'],
    )
    return {'translation': ''.join(item.translated_text for item in response.translations)}
