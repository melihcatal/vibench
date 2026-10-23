import os
import deepl

def translate_query(query: str, target_lang: str = "EN-US") -> str:
    """
    Translates a query to a target language using the DeepL API.
    
    Args:
        query: The text to translate.
        target_lang: The target language code (e.g., "EN-US", "DE", "FR").
        
    Returns:
        The translated text.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    
    # Provider-specific SDK import and client: deepl.Translator
    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(query, target_lang=target_lang)
    
    return result.text
