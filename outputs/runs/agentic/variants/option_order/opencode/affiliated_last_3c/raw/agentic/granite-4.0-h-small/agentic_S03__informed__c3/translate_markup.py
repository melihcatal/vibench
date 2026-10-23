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


def translate_markup(
    text: str, source_lang: str = "EN", target_lang: str = "FR"
) -> Dict:
    """Translate HTML/markup while preserving tags using the DeepL API.

    Args:
        text (str): Source markup string.
        source_lang (str): ISO 639-1 code of source language (default "EN").
        target_lang (str): ISO 639-1 code of target language (default "FR").

    Returns:
        Dict: Raw response containing translated markup.
    """
    client = DeepL(auth_key=DEEPL_AUTH_KEY)
    # Use preserve_formatting=True to keep tags intact
    result = client.translate(
        text=text,
        source_lang=source_lang,
        target_lang=target_lang,
        preserve_formatting=True,
    )
    return result
