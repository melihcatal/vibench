import os
from google.cloud import translate_v2 as translate

def translate_runbook_notes(text: str, target_language: str = "es", project_id: str = None) -> str:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation API.
    
    Args:
        text: The runbook notes to translate.
        target_language: Target language code (e.g., "es" for Spanish).
        project_id: Google Cloud project ID. Defaults to GOOGLE_CLOUD_PROJECT env var.
    
    Returns:
        Translated text.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    client = translate.Client(project=project_id)
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]