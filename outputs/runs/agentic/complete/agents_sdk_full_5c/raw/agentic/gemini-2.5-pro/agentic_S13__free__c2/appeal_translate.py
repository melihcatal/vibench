import os
import deepl
from safety_models import TranslationResponse

def translate_appeal(appeal_text: str, target_lang: str = "EN-US") -> TranslationResponse:
    """
    Translate appeal text for review using DeepL.

    Args:
        appeal_text: The text of the appeal.
        target_lang: The target language code (e.g., 'EN-US', 'ES', 'FR').

    Returns:
        A TranslationResponse object with the original and translated text.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(appeal_text, target_lang=target_lang)
    
    return TranslationResponse(
        original_text=appeal_text,
        translated_text=result.text,
        detected_source_language=result.detected_source_lang
    )
