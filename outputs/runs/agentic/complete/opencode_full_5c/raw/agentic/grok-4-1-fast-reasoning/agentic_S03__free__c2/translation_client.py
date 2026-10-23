import os
from typing import Optional
import deepl


def get_translator() -> deepl.Translator:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set.")
    return deepl.Translator(auth_key)
