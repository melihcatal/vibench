import os
import deepl
from security_models import TranslationResult


def translate_runbook(text: str, target_lang: str = "en") -> TranslationResult:
    """Translates secret-rotation runbook notes using DeepL API.

    Args:
        text: The runbook text to translate.
        target_lang: The target language code (e.g., 'en', 'de', 'es'). Defaults to 'en'.

    Returns:
        A TranslationResult object containing the translated text.

    Raises:
        Exception: If the DEEPL_AUTH_KEY is not set or API call fails.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return TranslationResult(translated_text=result.text)
    except Exception as e:
        raise Exception(f"DeepL API call failed: {e}")
