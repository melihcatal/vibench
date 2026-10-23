import deepl
import os
from typing import List, Optional

def batch_translate(texts: List[str], source_lang: Optional[str] = "auto", target_lang: str) -> List[str]:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    results = translator.translate_text(texts, source_lang=source_lang, target_lang=target_lang)
    return [result.text for result in results]
