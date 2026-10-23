import os
from google.cloud import translate_v2 as translate

# Google Cloud Translation client
_translate_client = None

def _get_translate_client():
    global _translate_client
    if _translate_client is None:
        _translate_client = translate.Client(project=os.environ.get("GCP_PROJECT_ID"))
    return _translate_client

def translate_compliance_note(text: str, target_language: str = "en", source_language: str = None):
    client = _get_translate_client()

    # The translate method automatically detects the source language if not provided.
    translation = client.translate(text, target_language=target_language, source_language=source_language)

    return {
        "original_text": text,
        "translated_text": translation["translatedText"],
        "source_language": translation["detectedSourceLanguage"],
        "target_language": target_language,
        "translation_provider": "Google Cloud Translation AI"
    }
