import os
import deepl


def get_translator():
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    return deepl.Translator(auth_key)
