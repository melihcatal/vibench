from google.cloud import translate

def runbook_translate(text_to_translate: str, target_language: str, project_id: str) -> dict:
    client = translate.TranslationServiceClient()
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_to_translate],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "target_language_code": target_language,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)
    
    return {"translated_text": translations[0] if translations else ""}
