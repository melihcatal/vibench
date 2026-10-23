from typing import List, Optional
from deepl import Translator
from translation_client import load_deepl_api_key
from translation_models import normalize_language_code

def batch_translate(texts: List[str], source_lang: Optional[str] = None, target_lang: str) -> List[str]:
    api_key = load_deepl_api_key()
    translator = Translator(api_key)
    source_lang = normalize_language_code(source_lang)
    return [
        translator.translate_text(text, source_lang=source_lang, target_lang=target_lang).text
        for text in texts
    ]
