import os
import deepl
from typing import Optional

def translate_text(text: str, target_lang: str = "FR") -> Optional[str]:
    """
    Translates text to the target language using the DeepL API.
    
    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "FR" for French).
        
    Returns:
        The translated text, or None if translation fails.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
        
    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        
        if isinstance(result, deepl.TextResult):
            return result.text
        # Handle cases where the input might be a list
        if isinstance(result, list) and result:
            return result[0].text
            
    except deepl.DeepLException as e:
        print(f"An error occurred with the DeepL API: {e}")
    
    return None
