import os
from typing import List, Optional
from google.cloud import translate_v3 as translate
from translation_client import get_translation_client, get_project_id, get_location
from translation_models import BatchTranslationResult

def batch_translate_texts(
    texts: List[str],
    target_language: str,
    source_language: Optional[str] = None,
    mime_type: str = "text/plain",
) -> BatchTranslationResult:
    client = get_translation_client()
    project_id = get_project_id()
    location = get_location()

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=texts,
        target_language_code=target_language,
        source_language_code=source_language,
        mime_type=mime_type,
    )

    translated_texts = [t.translated_text for t in response.translations]
    detected_source_languages = [t.detected_language_code for t in response.translations]

    return BatchTranslationResult(
        translated_texts=translated_texts,
        detected_source_languages=detected_source_languages,
    )
