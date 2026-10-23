import os
from functools import lru_cache

import deepl


@lru_cache(maxsize=1)
def get_translator() -> deepl.Translator:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    return deepl.Translator(auth_key)


def get_target_language_code(language: str) -> str:
    return language.upper()
