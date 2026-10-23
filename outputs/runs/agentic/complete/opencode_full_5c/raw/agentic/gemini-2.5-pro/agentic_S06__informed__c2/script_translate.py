import os
import deepl


def translate_narration_script(text: str, target_lang: str = "DE"):
    """Translates text into the target language using DeepL."""
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
