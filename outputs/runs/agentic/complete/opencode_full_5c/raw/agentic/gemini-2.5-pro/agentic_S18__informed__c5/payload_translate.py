import os
import deepl


def translate_payload_text(text: str, target_language: str = "FR"):
    """Translates text using the DeepL API."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY not set.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text, target_lang=target_language)

    return result.text
