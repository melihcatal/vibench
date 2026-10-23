import os
import deepl
from typing import tuple


def get_supported_languages() -> tuple[list[str], list[str]]:
    """
    Get supported source and target languages from DeepL.
    """
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    source_langs = [lang.code for lang in translator.get_source_languages()]
    target_langs = [lang.code for lang in translator.get_target_languages()]
    return source_langs, target_langs


def validate_target_lang(lang: str) -> bool:
    """
    Check if target language is supported.
    """
    _, target_langs = get_supported_languages()
    return lang.upper() in target_langs
