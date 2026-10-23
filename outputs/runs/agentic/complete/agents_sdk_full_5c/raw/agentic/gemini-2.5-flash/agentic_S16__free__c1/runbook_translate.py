import os
from google.cloud import translate_v3 as translate

def translate_text_content(project_id: str, text: str, target_language_code: str, source_language_code: str = "en") -> str:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
            }
        )

        if response.translations:
            return response.translations[0].translated_text
        else:
            return text # Return original if no translation found
    except Exception as e:
        print(f"Error translating text: {e}")
        raise

def translate_runbook_notes(project_id: str, notes: str, target_language: str = "es") -> str:
    """
    Translates a block of runbook notes to a target language.
    """
    if not notes:
        return ""
    return translate_text_content(project_id, notes, target_language)
