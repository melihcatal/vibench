# [LATER-STEP] ocr_translate.py
"""Translate extracted OCR text using a translation API (e.g., Google Cloud Translation)"""

import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate


# Configuration can be loaded from env vars or helpers
def get_translate_client() -> translate.Client:
    """Create a Google Cloud Translation client"""
    return translate.Client()


def translate_text(source_text: str, target_lang: str = "en") -> str:
    """Translate plain OCR text"""
    client = get_translate_client()
    result = client.translate(source_text, target_language=target_lang)
    return result["translatedText"]


if __name__ == "__main__":
    import json, sys

    # CLI usage: python ocr_translate.py <json-response> <target>
    if len(sys.argv) < 3:
        print("Usage: python ocr_translate.py <ocr-json> <target_language>")
        sys.exit(1)
    with open(sys.argv[1], "r") as f:
        ocr_json = json.load(f)
    text = ocr_json["Blocks"][0]["Text"] if ocr_json.get("Blocks") else ""
    target = sys.argv[2]
    print(translate_text(text, target))
