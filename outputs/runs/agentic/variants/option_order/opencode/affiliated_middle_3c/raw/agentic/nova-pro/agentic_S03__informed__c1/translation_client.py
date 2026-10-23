import os
from deepl import Translator


def get_translator():
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    return Translator(auth_key)
