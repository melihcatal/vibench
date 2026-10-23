import os
import requests
from vision_models import ImageDescriptionResponse

def alt_text_translate(description_response: ImageDescriptionResponse, target_language: str) -> str:
    """Translates generated image descriptions using DeepL API."""
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable not set.")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"DeepL-Auth-Key {api_key}"
    }
    
    payload = {
        "text": [description_response.description],
        "target_lang": target_language
    }
    
    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    
    return response.json()["translations"][0]["text"]