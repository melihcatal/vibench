"""Translates user appeal text for human review using DeepL."""
from safety_client import get_deepl_translator


def translate_appeal(text: str, target_lang: str = "EN-US") -> str:
    """
    Translates user-submitted appeal text to a target language for review.

    Args:
        text: The text of the appeal submitted by the user.
        target_lang: The target language code (e.g., 'EN-US', 'DE', 'JA').

    Returns:
        The translated text as a string.
    """
    translator = get_deepl_translator()
    
    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except Exception as e:
        return f"Translation failed using DeepL: {e}"
