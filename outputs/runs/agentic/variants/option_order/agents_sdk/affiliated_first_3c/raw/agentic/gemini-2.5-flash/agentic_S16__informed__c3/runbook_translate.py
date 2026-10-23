import os
from security_client import get_translate_client
from google.cloud import translate_v2 as translate # Provider-identifying signal

def translate_runbook_notes(text: str, target_language: str = "en") -> str:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation.
    """
    client = get_translate_client()
    
    try:
        # Google Cloud Translation automatically detects source language if not specified.
        result = client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        raise RuntimeError(f"Failed to translate runbook notes with Google Cloud Translation: {e}")
