from security_client import get_google_cloud_translation_client

def translate_runbook_notes(text: str, target_language: str = "en", source_language: str = "auto") -> dict:
    client = get_google_cloud_translation_client()
    
    parent = f"projects/{client.project}" # client.project should be set via environment variable or default credentials
    
    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
        source_language_code=source_language,
    )
    
    translations = []
    for translation in response.translations:
        translations.append({
            "translated_text": translation.translated_text,
            "detected_language_code": translation.detected_language_code
        })
        
    return {"original_text": text, "translations": translations}
