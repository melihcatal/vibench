import os
from typing import Dict

# Example using DeepL SDK (deepl)
try:
    from deepl import DeepL
except ImportError:
    raise ImportError("Install the DeepL SDK: pip install deepl")

# Load API key from environment (DeepL)
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise RuntimeError("Set the DEEPL_AUTH_KEY environment variable")


def translate_text(text: str, source_lang: str = "EN", target_lang: str = "FR") -> Dict:
    """Translate a single text string between languages using the DeepL API.

    Args:
        text (str): The source text to translate.
        source_lang (str): ISO 639-1 code of the source language (default "EN").
        target_lang (str): ISO 639-1 code of the target language (default "FR").

    Returns:
        Dict: The raw response from the DeepL service.
    """
    client = DeepL(auth_key=DEEPL_AUTH_KEY)
    result = client.translate(
        text=text, source_lang=source_lang, target_lang=target_lang
    )
    return result
