from google.cloud import translate_v3 as translate


def record_translate(payload, config=None):
    config = config or {}
    client = translate.TranslationServiceClient()
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    response = client.translate_text(request={"parent": parent, "contents": [payload["text"]], "target_language_code": payload["target_language"]})
    return {"translated_text": response.translations[0].translated_text}
