import os
from deepl import DeepL

def translate_welcome(message: str, target_locale: str) -> str:
    """Translate onboarding copy into the user's locale using DeepL API.
    Returns the translated text.
    """
    deepl_key = os.getenv('DEEPL_AUTH_KEY')
    if not deepl_key:
        raise RuntimeError("DEEPL_AUTH_KEY environment variable not set")
    translator = DeepL(auth_key=deepl_key)
    result = translator.translate_text(message, target_lang=target_locale)
    return result.text
