import os
import deepl
from typing import Optional

def translate_onboarding_copy(text: str, target_locale: str) -> Optional[str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_locale)
    return result.text