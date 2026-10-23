from google.cloud import translate_v3 as translate

def dashboard_note_translate(payload, config=None):
    config = config or {}
    project_id = config.get("project_id")
    
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    text_to_translate = payload["note_text"]
    target_language_code = payload["target_locale"]
    source_language_code = payload.get("source_locale") # Optional

    if source_language_code:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text_to_translate],
                "mime_type": "text/plain",
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
            }
        )
    else:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text_to_translate],
                "mime_type": "text/plain",
                "target_language_code": target_language_code,
            }
        )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)
    
    return {"translated_notes": translations}
