import os
import requests
import json
from extract_text import extract_text_from_image

# -------------------------------------------------
# LATER-STEP: ocr_translate.py
# Translate extracted OCR text using Google Cloud Translation API
# -------------------------------------------------

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY environment variable for translation")

TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"

def translate_ocr_text(text: str, target_lang: str = "en") -> str:
    """Translates plain OCR text to the target language.","
    payload = {
        "q": text,
        "target": target_lang,
        "format": "text",
        "source": None  # auto-detect
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(
        TRANSLATE_URL,
        params={"key": GOOGLE_API_KEY},
        json=payload,
        headers=headers,
        timeout=30
    )
    response.raise_for_status()
    data = response.json()
    # Google returns translations under data["data"]["translations"][0]["translatedText"]
    translated = data["data"]["translations"][0]["translatedText"]
    return translated

# Example usage with the same‑scenario OCR extraction
# image_path = "path/to/image.png"
# raw_text = extract_text_from_image(image_path)
# translated = translate_ocr_text(raw_text, target_lang="fr")
# print(translated)
