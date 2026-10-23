import os
from typing import Dict, Any
import requests
from vision_client import get_openai_api_key


def translate_image_description(
    description: str, target_language: str = "es"
) -> Dict[str, Any]:
    """
    Translate generated image descriptions using DeepL API.

    Args:
        description: Original image description text
        target_language: Target language code (default: Spanish "es")

    Returns:
        Dictionary containing translated text and metadata
    """
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable not set")

    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/json",
    }

    payload = {"text": [description], "target_lang": target_language}

    response = requests.post(
        "https://api-free.deepl.com/v2/translate", headers=headers, json=payload
    )
    response.raise_for_status()

    result = response.json()

    translations = result.get("translations", [])
    if not translations:
        raise ValueError("No translation returned from DeepL API")

    return {
        "original_text": description,
        "translated_text": translations[0].get("text", ""),
        "target_language": target_language,
        "detected_source_language": translations[0].get(
            "detected_source_language", "en"
        ),
        "provider": "deepl",
        "api_version": "v2",
    }
