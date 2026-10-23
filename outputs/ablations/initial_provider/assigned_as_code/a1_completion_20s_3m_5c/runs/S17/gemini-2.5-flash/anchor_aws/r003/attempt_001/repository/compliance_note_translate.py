from google.cloud import translate_v3 as translate

def translate_compliance_note(project_id: str, text: str, target_language_code: str, source_language_code: str = None):
    client = translate.TranslationServiceClient()
    location = "global"  # Translation API is global
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code if source_language_code else "en", # Default to English if not provided
            "mime_type": "text/plain",
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)
    
    return {"translations": translations}