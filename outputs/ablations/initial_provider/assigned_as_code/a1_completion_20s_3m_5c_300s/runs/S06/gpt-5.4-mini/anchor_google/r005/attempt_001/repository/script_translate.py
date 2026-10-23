from google.cloud import translate_v3


def script_translate(payload, config=None):
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{payload['project_id']}/locations/{payload.get('location', 'global')}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [payload["text"]],
            "mime_type": "text/plain",
            "source_language_code": payload.get("source_language_code", "en"),
            "target_language_code": payload["target_language_code"],
        }
    )
    return {"translated_text": response.translations[0].translated_text}
