from typing import List
import deepl
import os


def translate_scripts(
    texts: List[str],
    target_lang: str,
    source_lang: str = None
) -> List[str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY must be set in environment variables.")

    translator = deepl.Translator(auth_key)
    results = translator.translate_text(
        texts, target_lang=target_lang, source_lang=source_lang
    )
    return [result.text for result in results]