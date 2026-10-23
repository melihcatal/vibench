import os
from typing import Optional
import deepl


def translate_text(
    text: str,
    target_lang: str = "DE",
    source_lang: Optional[str] = None
) -> Optional[str]:
    """
    Translate generated model output using DeepL API.
    
    Args:
        text: Text to translate.
        target_lang: Target language code (e.g., 'DE').
        source_lang: Source language code (e.g., 'EN'). Optional.
        
    Returns:
        Translated text or None if failed.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        return None

    translator = deepl.Translator(auth_key)
    try:
        result = translator.translate_text(
            text,
            target_lang=target_lang,
            source_lang=source_lang
        )
        return result.text
    except Exception:
        return None