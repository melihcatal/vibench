from google.cloud import translate_v3 as translate

def dashboard_note_translate(payload: dict, config: dict = None) -> dict:
    config = config or {}
    project_id = config.get("project_id")
    if not project_id:
        raise ValueError("project_id must be provided in config")

    client = translate.TranslationServiceClient()
    
    note_text = payload.get("note_text")
    target_language = payload.get("target_language", "es") # Default to Spanish
    
    if not note_text:
        raise ValueError("note_text must be provided in payload")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [note_text],
            "target_language_code": target_language,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append({
            "translated_text": translation.translated_text,
            "detected_language_code": translation.detected_language_code,
        })

    return {
        "original_text": note_text,
        "target_language": target_language,
        "translations": translations,
        "provider_used": "Google Cloud Translation API"
    }
