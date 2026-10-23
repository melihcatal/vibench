# [LATER-STEP] script_translate.py
# Translate narration scripts before synthesis using DeepL API
import os
from deepl import DeepL
from typing import List

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise RuntimeError("Set DEEPL_AUTH_KEY environment variable for translation")


def translate_script(text: str, target_lang: str = "en") -> str:
    """Translate a single script or list of strings using DeepL."""
    if isinstance(text, list):
        return [translate_script(t, target_lang) for t in text]
    try:
        with DeepL(auth_key=DEEPL_AUTH_KEY) as translator:
            result = translator.translate_text(text, target_lang=target_lang)
            return result["text"]
    except Exception as e:
        raise RuntimeError(f"Translation failed: {e}")


# Example batch helper


def translate_batch(scripts: List[str], target_lang: str = "en") -> List[str]:
    return translate_script(scripts, target_lang)


if __name__ == "__main__":
    sample = "Hello, this is a test."
    print("Translated:", translate_script(sample))
