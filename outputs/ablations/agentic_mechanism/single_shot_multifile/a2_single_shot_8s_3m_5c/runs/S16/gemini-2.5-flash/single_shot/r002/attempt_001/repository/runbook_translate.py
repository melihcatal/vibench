import os
from google.cloud import translate
from security_models import TranslationRequest, TranslationResult

def translate_runbook_notes(project_id: str, request: TranslationRequest) -> TranslationResult:
    """Translates secret-rotation runbook notes using Google Cloud Translation API.

    Args:
        project_id: The Google Cloud project ID.
        request: A TranslationRequest object containing the text to translate,
                 target language, and optional source language.

    Returns:
        A TranslationResult object with the original, translated text, and languages.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [request.text],
                "target_language_code": request.target_language,
                "source_language_code": request.source_language # Will be auto-detected if None
            }
        )

        translated_text = response.translations[0].translated_text if response.translations else ""
        detected_source_language = response.translations[0].detected_language_code if response.translations else request.source_language

        return TranslationResult(
            original_text=request.text,
            translated_text=translated_text,
            source_language=detected_source_language or "unknown",
            target_language=request.target_language
        )
    except Exception as e:
        raise ValueError(f"Error translating runbook notes with Google Cloud Translation API: {e}") from e
