import os
import requests
from typing import Dict, Any
from vision_models import ImageDescriptionResponse


def translate_description(description: str, target_language: str) -> str:
    """Translate generated image descriptions using DeepL API."""
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable not set.")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"DeepL-Auth-Key {api_key}"
    }
    
    payload = {
        "text": [description],
        "target_lang": target_language
    }
    
    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    
    return response.json()["translations"][0]["text"]