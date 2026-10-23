import os
import deepl
from typing import Optional

def translate_compliance_note(note: str, target_lang: str = "ES", source_lang: Optional[str] = None) -> str:
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(
        note,
        target_lang=target_lang,
        source_lang=source_lang
    )
    
    return result.text
