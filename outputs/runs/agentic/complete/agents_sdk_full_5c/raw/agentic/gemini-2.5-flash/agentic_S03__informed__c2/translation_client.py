import deepl
import os

def get_deepl_client():
    """
    Initializes and returns a DeepL Translator client.
    Requires the DEEPL_AUTH_KEY environment variable to be set.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    return deepl.Translator(auth_key)
