import os
import deepl  # Provider SDK import


def translate_text(text: str, target_lang: str = "en") -> str:
    """
    Translates generated model output using DeepL.
    """
    auth_key = os.environ.get(
        "DEEPL_AUTH_KEY"
    )  # Provider-specific environment variable
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
