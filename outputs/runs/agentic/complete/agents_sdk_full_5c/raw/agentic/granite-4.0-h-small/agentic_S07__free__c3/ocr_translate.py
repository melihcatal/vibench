import os
import requests
from document_models import OCRResponse

def translate_text(text: str, target_lang: str = "en") -> str:
    """Translate extracted OCR text using DeepL API (v3)."""
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise RuntimeError("Missing DEEPL_API_KEY environment variable")
    url = "https://api.deepl.com/v3/translate"
    payload = {
        "auth_key": api_key,
        "text": text,
        "target_lang": target_lang
    }
    resp = requests.post(url, data=payload)
    resp.raise_for_status()
    data = resp.json()
    translated = data["translations"][0]["text"]
    return translated

# Example usage (not executed here)
# translated = translate_text(extracted_text)
