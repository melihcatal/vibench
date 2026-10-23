import os

def load_deepl_api_key() -> str:
    key = os.getenv("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")
    return key
