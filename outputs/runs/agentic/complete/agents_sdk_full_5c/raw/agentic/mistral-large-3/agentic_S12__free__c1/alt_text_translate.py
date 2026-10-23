import os
import requests
from vision_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    """Translates generated image descriptions using DeepL API."""
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable not set.")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"DeepL-Auth-Key {api_key}"
    }
    
    payload = {
        "text": [request.text],
        "target_lang": request.target_language
    }
    
    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    
    translated_text = response.json()["translations"][0]["text"]
    return TranslationResponse(
        provider="deepl",
        translated_text=translated_text
    )