import os
import deepl


def translate_onboarding_copy(text: str, target_locale: str) -> str:
    """Translates onboarding copy into the user's locale using DeepL."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_locale.upper())
    return result.text
