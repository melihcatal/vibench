import os
from typing import Dict, List
import requests
from .document_models import OCRResponse


def translate_text(text: str, target_language: str = "es") -> str:
    """
    Translates extracted OCR text using DeepL API.
    Requires DEEPL_AUTH_KEY environment variable.
    """
    api_key = os.getenv("DEEPL_AUTH_KEY")
    if not api_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")

    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/json",
    }
    data = {"text": [text], "target_lang": target_language}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["translations"][0]["text"]


def ocr_translate(
    ocr_response: OCRResponse, target_language: str = "es"
) -> Dict[str, str]:
    """
    Translates all text blocks from an OCR response using DeepL API.
    """
    translated_full_text = translate_text(ocr_response.full_text, target_language)
    translated_blocks = []
    for block in ocr_response.blocks:
        translated_text = translate_text(block.text, target_language)
        translated_blocks.append({**block.dict(), "text": translated_text})

    return {"full_text": translated_full_text, "blocks": translated_blocks}
