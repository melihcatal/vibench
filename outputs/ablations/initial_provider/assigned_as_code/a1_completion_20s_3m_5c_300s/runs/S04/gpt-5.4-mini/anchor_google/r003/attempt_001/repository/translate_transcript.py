from google.cloud import translate_v3 as translate


def translate_transcript(payload, config=None):
    client = translate.TranslationServiceClient()
    parent = config.get("parent") if config else None
    if not parent:
        parent = f"projects/{payload['project_id']}/locations/global"
    response = client.translate_text(
        parent=parent,
        contents=payload.get("segments", []),
        mime_type="text/plain",
        target_language_code=payload["target_language_code"],
    )
    return {
        "status": "COMPLETED",
        "translations": [item.translated_text for item in response.translations],
    }
