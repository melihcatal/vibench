import os
from typing import List
from deepl import Translator

def batch_translate(texts: List[str], source_lang: str = None, target_lang: str) -> List[str]:
    translator = Translator(os.getenv("DEEPL_AUTH_KEY"))
    results = translator.translate_text(texts, source_lang=source_lang, target_lang=target_lang)
    return [result.text for result in results]