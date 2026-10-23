import os
import deepl


def translate_output(text: str, target_lang: str = "en") -> str:
    """Translate platform model output for another locale using DeepL API."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
