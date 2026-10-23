import os
import requests
from vision_models import TranslatedDescriptionResponse


def translate_description(text: str, target_language: str) -> TranslatedDescriptionResponse:
    """Translate generated image descriptions using DeepL API."""
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable not set.")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"DeepL-Auth-Key {api_key}"
    }
    
    payload = {
        "text": [text],
        "target_lang": target_language
    }
    
    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    
    translated_text = response.json()["translations"][0]["text"]
    return TranslatedDescriptionResponse(
        original_text=text,
        translated_text=translated_text,
        target_language=target_language
    )