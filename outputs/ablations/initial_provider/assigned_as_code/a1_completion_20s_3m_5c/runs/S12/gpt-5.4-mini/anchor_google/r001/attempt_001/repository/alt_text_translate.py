from google.cloud import translate_v3 as translate


def alt_text_translate(payload, config=None):
    config = config or {}
    client = translate.TranslationServiceClient()
    parent = client.location_path(config.get("project_id"), config.get("location", "global"))
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [payload.get("text", "")],
            "mime_type": "text/plain",
            "target_language_code": config.get("target_language", "en"),
        }
    )
    return {"translated_text": response.translations[0].translated_text if response.translations else ""}
