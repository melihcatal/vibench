import os
import deepl


def translate_description(description: str, target_lang: str = "DE") -> str:
    """Translates the image description to a target language using DeepL."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(description, target_lang=target_lang)
    return result.text
