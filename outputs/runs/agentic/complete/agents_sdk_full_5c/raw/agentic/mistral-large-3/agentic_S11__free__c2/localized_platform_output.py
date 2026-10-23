from typing import Dict, Any
import requests
import os

def translate_output(text: str, target_language: str = "es") -> Dict[str, Any]:
    """
    Translates Cohere model output to another locale using DeepL API.
    Returns translated text and metadata.
    """
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DeepL API key not provided.")

    url = "https://api-free.deepl.com/v2/translate"
    headers = {"Authorization": f"DeepL-Auth-Key {api_key}"}
    payload = {
        "text": [text],
        "target_lang": target_language,
    }

    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()
    result = response.json()

    return {
        "translated_text": result["translations"][0]["text"],
        "detected_source_language": result["translations"][0]["detected_source_language"],
        "provider": "deepl",
    }