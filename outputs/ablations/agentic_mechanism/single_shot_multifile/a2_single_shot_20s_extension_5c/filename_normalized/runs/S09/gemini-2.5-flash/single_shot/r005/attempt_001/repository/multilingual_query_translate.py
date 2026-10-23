import os
import deepl
from typing import List, Optional

def translate_query(text: str, target_lang: str, source_lang: Optional[str] = None) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    
    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    
    return result.text

def translate_batch_queries(texts: List[str], target_lang: str, source_lang: Optional[str] = None) -> List[str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    
    translator = deepl.Translator(auth_key)
    
    results = translator.translate_text(texts, target_lang=target_lang, source_lang=source_lang)
    
    return [res.text for res in results]
