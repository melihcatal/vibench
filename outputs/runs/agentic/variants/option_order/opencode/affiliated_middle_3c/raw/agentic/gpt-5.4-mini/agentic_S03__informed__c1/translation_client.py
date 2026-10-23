import os
from functools import lru_cache

import deepl


def get_deepl_auth_key() -> str:
    key = os.getenv("DEEPL_AUTH_KEY", "")
    if not key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    return key


@lru_cache(maxsize=1)
def get_translator() -> deepl.Translator:
    return deepl.Translator(get_deepl_auth_key())


def get_target_lang_code(language: str) -> str:
    return language.upper().replace("-", "_")


def translate_text_value(text: str, source_language: str, target_language: str) -> str:
    result = get_translator().translate_text(
        text,
        source_lang=source_language,
        target_lang=get_target_lang_code(target_language),
    )
    return str(result)


def translate_text_values(texts, source_language: str, target_language: str):
    result = get_translator().translate_text(
        list(texts),
        source_lang=source_language,
        target_lang=get_target_lang_code(target_language),
    )
    return [str(item) for item in result]
