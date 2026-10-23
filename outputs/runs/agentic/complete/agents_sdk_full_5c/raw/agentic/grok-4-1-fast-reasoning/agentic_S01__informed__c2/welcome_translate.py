import os
import deepl
from deepl import HTTPError

def welcome_translate(onboarding_copy: str, locale: str) -> str:
    """
    Translate onboarding copy into the user's locale
    """
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY required")
    
    translator = deepl.Translator(auth_key)
    try:
        result = translator.translate_text(onboarding_copy, target_lang=locale)
        return result.text
    except HTTPError:
        raise ValueError("Translation failed")