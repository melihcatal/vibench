from google.cloud import translate_v3 as translate


def script_translate(payload, config=None):
    config = config or {}
    client = translate.TranslationServiceClient()
    parent = client.location_path(config.get("project_id"), config.get("location", "global"))
    response = client.translate_text(
        parent=parent,
        contents=[payload["text"]],
        mime_type="text/plain",
        source_language_code=config.get("source_language_code", "en"),
        target_language_code=config.get("target_language_code", "en"),
    )
    return {"text": response.translations[0].translated_text, "provider": "google_translate_v3"}
