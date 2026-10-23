from google.cloud import translate_v3 as translate


def log_message_translate(payload, config=None):
    client = translate.TranslationServiceClient()
    parent = f"projects/{payload['project_id']}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [payload["text"]],
            "mime_type": "text/plain",
            "source_language_code": payload.get("source_language_code"),
            "target_language_code": payload["target_language_code"],
        }
    )
    return {"translated_text": response.translations[0].translated_text}
