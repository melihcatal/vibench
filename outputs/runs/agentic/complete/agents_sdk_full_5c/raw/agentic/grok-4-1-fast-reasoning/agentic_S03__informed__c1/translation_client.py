import os
from deepl import Translator

def get_translator() -> Translator:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")
    return Translator(auth_key)