from google.cloud import translate_v3 as translate


def translate_transcript(payload, config=None):
    config = config or {}
    client = translate.TranslationServiceClient()
    parent = f"projects/{payload['project_id']}/locations/{payload.get('location', 'global')}"
    response = client.translate_text(
        contents=[payload["text"]],
        target_language_code=payload["target_language_code"],
        parent=parent,
    )
    translations = [item.translated_text for item in response.translations]
    return {"status": "COMPLETED", "translations": translations}
