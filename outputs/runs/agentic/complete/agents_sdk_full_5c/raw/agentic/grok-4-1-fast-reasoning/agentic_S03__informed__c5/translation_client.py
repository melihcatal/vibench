import os

def ensure_deepl_auth() -> str:
    """
    Ensure DeepL authentication key is available.
    """
    key = os.getenv("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set.")
    return key
