from google.cloud import translate_v3


def log_message_translate(payload, config=None):
    client = translate_v3.TranslationServiceClient()
    project_id = (config or {}).get("project_id")
    location = (config or {}).get("location", "global")
    parent = f"projects/{project_id}/locations/{location}"
    text = payload.get("text", "")
    target = payload.get("target_language", "es")
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target,
        }
    )
    return {"text": text, "translated": response.translations[0].translated_text if response.translations else "", "target_language": target}
