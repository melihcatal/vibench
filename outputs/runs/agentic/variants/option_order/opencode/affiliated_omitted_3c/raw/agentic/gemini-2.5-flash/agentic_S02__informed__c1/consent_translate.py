import os
import deepl

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


def translate_consent_copy(text: str, target_lang: str = "en") -> str:
    if not DEEPL_AUTH_KEY:
        raise ValueError("Missing DEEPL_AUTH_KEY environment variable")

    translator = deepl.Translator(DEEPL_AUTH_KEY)

    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except Exception as e:
        return f"Error translating text: {e}"
