import deepl
import os


def translate_runbook_notes(text: str, target_lang: str = "EN-US") -> str:
    """
    Translates secret-rotation runbook notes using DeepL API.
    
    Args:
        text: The text to translate.
        target_lang: The target language code (default: "EN-US").
        
    Returns:
        The translated text as a string.
    """
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text