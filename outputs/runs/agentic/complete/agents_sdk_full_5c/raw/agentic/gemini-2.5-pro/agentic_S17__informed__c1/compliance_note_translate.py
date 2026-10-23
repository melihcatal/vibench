# compliance_note_translate.py
import os
import deepl

def translate_compliance_note(text: str, target_lang: str) -> str:
    """
    Translates a compliance note to a target language using the DeepL API.
    
    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "FR", "ES", "DE").
    
    Returns:
        The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
        
    translator = deepl.Translator(auth_key)
    
    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred with the DeepL API: {e}")
        raise
