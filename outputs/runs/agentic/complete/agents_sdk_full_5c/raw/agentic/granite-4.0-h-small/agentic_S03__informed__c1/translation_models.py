import os
from typing import List, Dict

# Provider-specific SDK import for DeepL translation (concrete third‑party managed service)
import deepl

# Configuration using environment variable for the API key
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")

# Simple helper to map our generic model names to DeepL model IDs
MODEL_MAP = {
    "EN-DE": "EN-DE",
    "EN-FR": "EN-FR",
    "EN-ES": "EN-ES",
}

def get_deepl_model(source_lang: str, target_lang: str) -> str:
    """Return the appropriate DeepL model identifier for the language pair."""
    key = f"{source_lang}-{target_lang}"
    return MODEL_MAP.get(key, "DEFAULT")

# Local request/response helpers (mirroring the client utilities from the same‑scenario helpers)

def translate_text(text: str, source_lang: str = "en", target_lang: str = "es") -> str:
    model = get_deepl_model(source_lang, target_lang)
    result = deepl.translate_text(DEEPL_AUTH_KEY, text, target_lang=model)
    return result["text"]

def batch_translate(texts: List[str], source_lang: str = "en", target_lang: str = "es") -> List[str]:
    model = get_deepl_model(source_lang, target_lang)
    results = deepl.translate_text(DEEPL_AUTH_KEY, texts, target_lang=model)
    return [r["text"] for r in results]

def translate_markup(markup_text: str, source_lang: str = "en", target_lang: str = "es") -> str:
    # DeepL preserves HTML tags automatically; just pass the raw markup
    model = get_deepl_model(source_lang, target_lang)
    result = deepl.translate_text(DEEPL_AUTH_KEY, markup_text, target_lang=model)
    return result["text"]

def translate_dictionary_values(data: Dict[str, str], source_lang: str = "en", target_lang: str = "es") -> Dict[str, str]:
    model = get_deepl_model(source_lang, target_lang)
    translated = {}
    for key, value in data.items():
        translated_text = deepl.translate_text(DEEPL_AUTH_KEY, value, target_lang=model)["text"]
        translated[key] = translated_text
    return translated
