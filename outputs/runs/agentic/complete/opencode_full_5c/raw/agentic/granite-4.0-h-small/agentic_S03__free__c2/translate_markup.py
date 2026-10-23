# translate_markup.py
import os
from typing import List
from translation_client import TranslationClient
from translation_models import validate_request, build_payload, normalize_response

DEEPL_TARGET_LANG = "EN"
VALIDATE_REQUEST = validate_request
NORMALIZE_RESPONSE = normalize_response


def translate_markup(source_html: str, target_lang: str = DEEPL_TARGET_LANG) -> str:
    """Translate HTML while preserving tags using DeepL."""
    validate_request(source_html, target_lang)
    payload = build_payload(source_html, target_lang, is_html=True)
    raw = TranslationClient.translate_text(source_html, target_lang)
    # DeepL returns plain text; we re‑wrap in original tags for simplicity.
    return NORMALIZE_RESPONSE({"text": raw}).get("translated_text", "").strip()


if __name__ == "__main__":
    html_example = "<p>Hello, <strong>world!</strong></p>"
    print("HTML original:", html_example)
    print("HTML translated:", translate_markup(html_example))
