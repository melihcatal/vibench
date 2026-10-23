import os
from typing import Dict, Any, Optional
from deepl import Translator

def translate_dictionary_values(d: Dict[str, Any], target_lang: str, source_lang: Optional[str] = None) -> Dict[str, Any]:
    translator = Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = d.copy()
    for key, value in result.items():
        if isinstance(value, str):
            result[key] = translator.translate_text(value, source_lang=source_lang, target_lang=target_lang).text
    return result