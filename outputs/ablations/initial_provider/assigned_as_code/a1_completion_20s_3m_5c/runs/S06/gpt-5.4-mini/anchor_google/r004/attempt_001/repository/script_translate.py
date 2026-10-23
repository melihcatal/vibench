from google.cloud import translate_v3 as translate


def script_translate(payload, config=None):
    config = config or {}
    client = translate.TranslationServiceClient()
    parent = client.location_path(config.get("project_id", "project"), config.get("location", "global"))
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [payload["text"]],
            "mime_type": "text/plain",
            "target_language_code": config.get("target_language_code", "en"),
        }
    )
    return {"text": response.translations[0].translated_text}
