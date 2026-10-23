import os
import requests
from typing import Dict


def translate_runbook_notes(text: str, target_language: str = "es") -> str:
    """
    Translates secret-rotation runbook notes using DeepL API.
    
    Args:
        text: The runbook notes to translate.
        target_language: The target language code (e.g., "es" for Spanish).
    
    Returns:
        The translated text.
    """
    deepl_api_key = os.getenv("DEEPL_API_KEY")
    if not deepl_api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required.")
    
    url = "https://api-free.deepl.com/v2/translate"
    headers = {"Authorization": f"DeepL-Auth-Key {deepl_api_key}"}
    payload = {
        "text": text,
        "target_lang": target_language,
    }
    
    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()["translations"][0]["text"]