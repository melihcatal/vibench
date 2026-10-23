import os
import deepl
from typing import Dict, Any

def invoice_note_translate(note: str, target_lang: str = 'EN') -> Dict[str, Any]:
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(note, target_lang=target_lang)
    return {
        'original': note,
        'translated': result.text,
        'detected_source_lang': result.detected_source_lang,
        'target_lang': target_lang
    }