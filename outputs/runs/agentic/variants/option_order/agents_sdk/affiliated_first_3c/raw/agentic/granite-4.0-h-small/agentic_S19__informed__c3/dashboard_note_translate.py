# dashboard_note_translate.py
# LATER-STEP: Translate metric or dashboard notes for another locale

import os
from typing import Dict, Any
import deepl

# DeepL API configuration via env vars
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise RuntimeError("Set DEEPL_AUTH_KEY environment variable")

# Instantiate the client once (singleton pattern)
class DeepLClient:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = deepl.Client(DEEPL_AUTH_KEY)
        return cls._instance
    def translate(self, text: str, target_lang: str = 'FR') -> str:
        return self.client.translate_text(text, target_lang=target_lang).text

translator = DeepLClient()


def translate_note(note: str, target_locale: str = 'fr') -> Dict[str, Any]:
    """
    Translates a free‑text note (metric label, dashboard description, etc.)
    using DeepL and returns a normalized dict suitable for downstream storage.
    """
    translated = translator.translate(note, target_lang=target_locale)
    return {
        "original": note,
        "target_locale": target_locale.upper(),
        "translated": translated,
        "translation_engine": "DeepL"
    }

# ---------------------------------------------------------------------------
# Example usage
if __name__ == "__main__":
    sample_note = "High CPU usage detected on the web tier."
    translation = translate_note(sample_note, target_locale='es')
    print(translation)
