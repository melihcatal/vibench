from observability_client import get_translate_client
from observability_models import TranslatedText
import os

def translate_dashboard_note(project_id: str, text: str, target_language_code: str, source_language_code: str = "en") -> TranslatedText:
    client = get_translate_client()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(TranslatedText(
            source_language_code=source_language_code,
            target_language_code=target_language_code,
            translated_text=translation.translated_text,
            original_text=text
        ))
    
    # Assuming only one text is passed, return the first translation.
    if translations:        return translations[0]
    else:        return TranslatedText(
            source_language_code=source_language_code,
            target_language_code=target_language_code,
            translated_text=text, # Fallback to original if no translation
            original_text=text
        )
