from google.cloud import translate_v3 as translate
from security_client import get_translation_client
from security_models import TranslationResult

def translate_runbook_notes(text: str, project_id: str, target_language: str = "en", source_language: str = "auto"):
    client = get_translation_client()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "source_language_code": source_language if source_language != "auto" else None,
            "target_language_code": target_language,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(TranslationResult(
            original_text=text,
            translated_text=translation.translated_text,
            source_language=translation.detected_language_code if source_language == "auto" else source_language,
            target_language=target_language
        ).__dict__)
    
    return {"translations": translations}
