import os
from typing import List, Dict, Any
from google.cloud import translate_v2 as translate

def translate_text(project_id: str, texts: List[str], target_language: str) -> List[Dict[str, Any]]:
    """
    Translates user-facing document fields using Google Cloud Translation API.

    Args:
        project_id: The Google Cloud project ID.
        texts: A list of strings to translate.
        target_language: The target language code (e.g., "es" for Spanish).

    Returns:
        A list of dictionaries, each containing the translated text and its detected source language.
    """
    translate_client = translate.Client(project=project_id)

    translations = translate_client.translate(
        texts,
        target_language=target_language
    )

    results = []
    for translation in translations:
        results.append({
            "translated_text": translation["translatedText"],
            "detected_source_language": translation["detectedSourceLanguage"]
        })
    return results
