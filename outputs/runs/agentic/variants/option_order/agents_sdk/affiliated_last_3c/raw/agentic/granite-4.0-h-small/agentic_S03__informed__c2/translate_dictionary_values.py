import os
from typing import Dict, Any
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse

def translate_dictionary_values(data: Dict[str, Any], source_lang: str = 'en', target_lang: str = 'es') -> Dict[str, Any]:
    """Translates all string values in a dictionary while preserving keys.
    Nested dictionaries are processed recursively.
    """
    client = get_translation_client()
    def _translate(value: Any, src: str, tgt: str) -> Any:
        if isinstance(value, str):
            req = TranslationRequest(text=value, source_lang=src, target_lang=tgt)
            resp: TranslationResponse = client.translate(req)
            return resp.translated_text
        elif isinstance(value, dict):
            return {k: _translate(v, src, tgt) for k, v in value.items()}
        elif isinstance(value, list):
            return [_translate(item, src, tgt) for item in value]
        else:
            return value
    return {k: _translate(v, source_lang, target_lang) for k, v in data.items()}
