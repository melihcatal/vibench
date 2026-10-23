import os
import requests
from typing import Dict, Optional


def translate_runbook_notes(text: str, target_language: str = "es") -> Optional[str]:
    """
    Translates secret-rotation runbook notes using DeepL's API.
    
    Args:
        text: The runbook notes to translate.
        target_language: Target language code (e.g., "es", "fr").
    
    Returns:
        Translated text as a string, or None if translation fails.
    """
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable not set.")
    
    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        data={
            "auth_key": api_key,
            "text": text,
            "target_lang": target_language
        }
    )
    response.raise_for_status()
    return response.json()["translations"][0]["text"]