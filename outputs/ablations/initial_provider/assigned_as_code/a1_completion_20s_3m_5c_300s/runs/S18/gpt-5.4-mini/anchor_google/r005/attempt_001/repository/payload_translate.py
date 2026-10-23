from google.cloud import translate_v3


def payload_translate(payload, config=None):
    config = config or {}
    text = payload.get("text", "")
    target_language = payload.get("target_language") or config.get("target_language", "en")
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{config.get('project_id')}/locations/{config.get('location', 'global')}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    translated = response.translations[0].translated_text if response.translations else ""
    return {"provider": "google_cloud_translation_v3", "translated_text": translated, "target_language": target_language}
