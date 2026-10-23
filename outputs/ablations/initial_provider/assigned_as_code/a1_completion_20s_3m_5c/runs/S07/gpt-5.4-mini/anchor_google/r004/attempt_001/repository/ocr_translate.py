from google.cloud import translate_v3


def ocr_translate(payload, config=None):
    config = config or {}
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [payload["text"]],
            "mime_type": "text/plain",
            "source_language_code": config.get("source_language_code", "en"),
            "target_language_code": config["target_language_code"],
        }
    )
    return {"translated_text": response.translations[0].translated_text}
