import os
import deepl
from typing import List, Optional
from translation_client import get_deepl_auth_key

def batch_translate(texts: List[str], source_lang: Optional[str] = None, target_lang: str) -> List[str]:
    auth_key = get_deepl_auth_key()
    translator = deepl.Translator(auth_key)
    return [
        translator.translate_text(text, target_lang=target_lang, source_lang=source_lang).text
        for text in texts
    ]
