import os
import deepl


def translate_dashboard_note(text: str, target_lang: str = "en"):  # Default to English
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text, target_lang=target_lang)

    return result.text
