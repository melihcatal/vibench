from google.cloud import translate_v3


def script_translate(payload, config=None):
    config = config or {}
    client = translate_v3.TranslationServiceClient()
    parent = config.get("parent")
    response = client.translate_text(
        parent=parent,
        contents=[payload["text"]],
        mime_type="text/plain",
        target_language_code=payload.get("target_language_code", "en"),
    )
    translations = [item.translated_text for item in response.translations]
    return {"translations": translations}
