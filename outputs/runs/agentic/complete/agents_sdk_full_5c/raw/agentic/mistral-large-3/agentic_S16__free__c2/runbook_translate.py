import os
import requests
from typing import Dict


def runbook_translate(text: str, target_language: str, api_key: str = None) -> str:
    """
    Translate secret-rotation runbook notes using DeepL API.
    
    Args:
        text: The runbook text to translate.
        target_language: Target language code (e.g., "DE", "FR").
        api_key: DeepL API key. Defaults to DEEPL_API_KEY env var.
    
    Returns:
        Translated text.
    """
    if api_key is None:
        api_key = os.getenv("DEEPL_API_KEY")
    
    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        data={
            "auth_key": api_key,
            "text": text,
            "target_lang": target_language
        }
    )
    
    return response.json()["translations"][0]["text"]