import os
import deepl
from typing import Dict, Optional
from translation_client import get_deepl_auth_key

def translate_dictionary_values(d: Dict[str, str], source_lang: Optional[str] = None, target_lang: str) -> Dict[str, str]:
    auth_key = get_deepl_auth_key()
    translator = deepl.Translator(auth_key)
    return {
        key: translator.translate_text(value, target_lang=target_lang, source_lang=source_lang).text
        for key, value in d.items()
    }
