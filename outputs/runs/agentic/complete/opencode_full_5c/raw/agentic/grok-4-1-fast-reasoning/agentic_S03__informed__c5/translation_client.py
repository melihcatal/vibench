import os
import deepl
from typing import Optional


def get_translator(auth_key: Optional[str] = None) -> deepl.Translator:
    key = auth_key or os.getenv("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError(
            "No DeepL auth key provided. Set DEEPL_AUTH_KEY environment variable."
        )
    return deepl.Translator(key)
