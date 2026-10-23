import os
from typing import Optional
from google.cloud import translate_v3 as translate
from translation_client import get_translation_client, get_project_id, get_location
from translation_models import TextTranslationResult

def translate_html_markup(
    html_content: str,
    target_language: str,
    source_language: Optional[str] = None,
) -> TextTranslationResult:
    client = get_translation_client()
    project_id = get_project_id()
    location = get_location()

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[html_content],
        target_language_code=target_language,
        source_language_code=source_language,
        mime_type="text/html",
    )

    translated_text = ""
    detected_source_language = None
    if response.translations:
        translated_text = response.translations[0].translated_text
        detected_source_language = response.translations[0].detected_language_code

    return TextTranslationResult(
        translated_text=translated_text,
        detected_source_language=detected_source_language,
    )
