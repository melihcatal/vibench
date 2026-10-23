import os
import deepl
from typing import Optional

translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))


def multilingual_query_translate(
    query: str, target_lang: str = "EN", source_lang: Optional[str] = None
) -> str:
    result = translator.translate_text(
        query, target_lang=target_lang, source_lang=source_lang
    )
    return result.text
