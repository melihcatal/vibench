
import os
import deepl

def translate_text(text: str, target_language: str = "FR") -> str:
    """
    Translates text to a target language using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
        
    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(text, target_lang=target_language)
    return result.text
