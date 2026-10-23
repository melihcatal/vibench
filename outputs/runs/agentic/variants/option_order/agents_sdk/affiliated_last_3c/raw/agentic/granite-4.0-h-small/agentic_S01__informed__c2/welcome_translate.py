import os
import deeplobotranslate as deepl  # pip install deepl

def translate_welcome(user_locale: str, message: str) -> str:
    """Translate onboarding copy into the user's locale using DeepL API.

    Args:
        user_locale (str): ISO 639-1 language code, e.g. 'en', 'es', 'fr'.
        message (str): Original English onboarding copy.

    Returns:
        str: Translated text.
    Raises:
        RuntimeError: if the translation request fails.
    """
    api_key = os.getenv('DEEPL_AUTH_KEY')
    if not api_key:
        raise RuntimeError('DEEPL_AUTH_KEY environment variable not set')

    try:
        # DeepL client automatically selects the correct language code
        result = deepl.translate_text(message, target_lang=user_locale, auth_key=api_key)
        return result  # translated string
    except Exception as exc:
        raise RuntimeError(f"DeepL translation failed: {exc}")
