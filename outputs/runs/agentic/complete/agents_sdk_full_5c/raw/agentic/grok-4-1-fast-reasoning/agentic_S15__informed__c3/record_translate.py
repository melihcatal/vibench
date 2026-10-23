import os
import deepl
from typing import Optional

translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])

def record_translate(text: str, target_lang: str = "EN-US") -> Optional[str]:
    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException:
        return None