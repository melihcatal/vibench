
import os
import deepl
from typing import List

def translate_text(
    text_list: List[str],
    target_language: str = "EN-US"
) -> List[str]:
    """
    Translates a list of texts using the DeepL API.
    
    Reads API key from DEEPL_AUTH_KEY environment variable.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
        
    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(text_list, target_lang=target_language)
    
    if isinstance(result, list):
        return [translation.text for translation in result]
    else:
        return [result.text]
