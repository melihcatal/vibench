from google.cloud import translate
import os

def translate_output(text: str, target_language: str, project_id: str):
    """
    Translates platform model output for another locale using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()

    location = "global" # Or a specific region if preferred, e.g., "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)
    
    return {"original_text": text, "translated_text": translations[0] if translations else "", "target_language": target_language}
