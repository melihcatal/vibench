import os
import requests
from observability_models import TranslationResult

API_ENDPOINT = "https://api.deepl.com/v2/translate"
AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
TARGET_LANG = "FR"  # example target locale

if not AUTH_KEY:
    raise RuntimeError("DEEPL_AUTH_KEY environment variable is not set")


def translate_message(text: str, target_lang: str = TARGET_LANG) -> TranslationResult:
    """Translate support‑visible log messages for another locale using DeepL API.
    Returns a TranslationResult with the translated text and detected source language.
    """
    payload = {"auth_key": AUTH_KEY, "text": text, "target_lang": target_lang}
    response = requests.post(API_ENDPOINT, data=payload)
    response.raise_for_status()
    data = response.json()
    source_lang = data["source_lang"]
    translated = data["translations"][0]["text"]
    return TranslationResult(
        source=source_lang, target=target_lang, translated_text=translated
    )
