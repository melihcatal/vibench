import os
import requests
from typing import Dict, Any


def compliance_note_translate(text: str, target_language: str = "es") -> Dict[str, Any]:
    """
    Translates encryption or compliance notes using DeepL API.

    Args:
        text: Text to translate.
        target_language: Target language code (e.g., 'es', 'fr', 'de').

    Returns:
        Dictionary containing translated text and metadata.
    """
    api_key = os.getenv("DEEPL_AUTH_KEY")
    if not api_key:
        raise ValueError("DeepL API key must be set.")

    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/json",
    }

    body = {"text": [text], "target_lang": target_language}

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

    result = response.json()
    return {
        "translated_text": result["translations"][0]["text"],
        "detected_source_language": result["translations"][0][
            "detected_source_language"
        ],
        "target_language": target_language,
    }
