import os
import requests
from typing import Dict, Any
from vision_models import ImageDescriptionResponse

def translate_text(text: str, target_language: str) -> str:
    """Translates text using DeepL API."""
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable not set.")
    
    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}"
    }
    
    payload = {
        "text": text,
        "target_lang": target_language
    }
    
    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()["translations"][0]["text"]

def alt_text_translate(description: ImageDescriptionResponse, target_language: str) -> Dict[str, Any]:
    """Translates generated image descriptions using DeepL API."""
    translated_text = translate_text(description.description, target_language)
    
    return {
        "original_provider": description.provider,
        "original_description": description.description,
        "translated_description": translated_text,
        "target_language": target_language
    }