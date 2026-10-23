import os
from google.cloud import translate_v2 as translate

# Configure Google Cloud Translation API
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set

def translate_text(text: str, target_language: str = "en"):
    if not text:
        return {"status": "success", "translated_text": "", "message": "No text to translate."}

    translate_client = translate.Client()

    try:
        response = translate_client.translate(
            text,
            target_language=target_language
        )
        return {"status": "success", "translated_text": response["translatedText"], "source_language": response["detectedSourceLanguage"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def translate_document_fields(document: dict, fields_to_translate: list[str], target_language: str = "en"):
    translated_document = document.copy()
    
    for field in fields_to_translate:
        if field in translated_document and isinstance(translated_document[field], str):
            translation_result = translate_text(translated_document[field], target_language)
            if translation_result["status"] == "success":
                translated_document[field] = translation_result["translated_text"]
            else:
                # Handle translation error for a specific field, perhaps log it
                print(f"Warning: Failed to translate field '{field}': {translation_result["message"]}")
    
    return {"status": "success", "translated_document": translated_document}
