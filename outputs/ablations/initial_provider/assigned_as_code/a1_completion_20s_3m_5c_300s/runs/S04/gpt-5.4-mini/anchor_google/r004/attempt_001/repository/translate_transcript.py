from google.cloud import translate_v3 as translate


def translate_transcript(payload, config=None):
    config = config or {}
    client = translate.TranslationServiceClient()
    parent = f"projects/{config.get('project_id')}/locations/{config.get('location', 'global')}"
    response = client.translate_text(
        parent=parent,
        contents=payload["segments"],
        mime_type="text/plain",
        source_language_code=payload["source_language_code"],
        target_language_code=payload["target_language_code"],
    )
    return {"translations": [item.translated_text for item in response.translations]}
