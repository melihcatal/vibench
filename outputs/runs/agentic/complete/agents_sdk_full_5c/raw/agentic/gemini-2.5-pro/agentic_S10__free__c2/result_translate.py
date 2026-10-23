import os
import deepl

def translate_text(text: str, target_language_code: str = "DE") -> str:
    """
    Translates text to a target language using the DeepL API.
    
    Requires a DEEPL_AUTH_KEY environment variable.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    # Provider-specific client: deepl.Translator
    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(text, target_lang=target_language_code)
    
    return result.text
