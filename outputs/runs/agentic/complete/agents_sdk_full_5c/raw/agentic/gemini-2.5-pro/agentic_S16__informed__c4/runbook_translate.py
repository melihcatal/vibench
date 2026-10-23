import os
import deepl
from typing import Optional

def translate_runbook_notes(text: str, target_language: str = "JA") -> Optional[str]:
    """
    Translates secret-rotation runbook notes to a target language using DeepL.

    Args:
        text: The runbook text to translate.
        target_language: The target language code (e.g., "JA" for Japanese).

    Returns:
        The translated text, or None if translation fails.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        return None

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException:
        return None
