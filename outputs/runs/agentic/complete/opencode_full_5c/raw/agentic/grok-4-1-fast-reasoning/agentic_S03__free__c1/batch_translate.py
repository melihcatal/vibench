import deepl
import os
from typing import List


def batch_translate(
    texts: List[str], source_lang: str = "EN", target_lang: str = "ES"
) -> List[str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    results = translator.translate_text(
        texts, source_lang=source_lang, target_lang=target_lang
    )
    return [result.text for result in results]
