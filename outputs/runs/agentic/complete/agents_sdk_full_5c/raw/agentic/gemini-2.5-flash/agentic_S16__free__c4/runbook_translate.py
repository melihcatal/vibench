from google.cloud import translate_v3 as translate
import os
from typing import List, Dict

def translate_runbook_notes(
    project_id: str,
    texts: List[str],
    target_language_code: str,
    source_language_code: str = None,
    model: str = "nmt" # Neural Machine Translation
) -> List[Dict[str, str]]:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    translations = []
    for text in texts:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
                "source_language_code": source_language_code,
                "model": f"projects/{project_id}/locations/global/models/{model}" if model else None,
            }
        )

        for translation in response.translations:
            translations.append({
                "original_text": text,
                "translated_text": translation.translated_text,
                "detected_source_language": translation.detected_language_code
            })
    return translations

