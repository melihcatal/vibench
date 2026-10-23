import os
from typing import List, Dict

# Example using DeepL SDK (deepl)
try:
    from deepl import DeepL
except ImportError:
    raise ImportError("Install the DeepL SDK: pip install deepl")

# Load API key from environment (DeepL)
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise RuntimeError("Set the DEEPL_AUTH_KEY environment variable")


def batch_translate(
    texts: List[str], source_lang: str = "EN", target_lang: str = "FR"
) -> List[Dict]:
    """Translate a list of strings while preserving order using the DeepL API.

    Args:
        texts (List[str]): List of source texts to translate.
        source_lang (str): ISO 639-1 code of the source language (default "EN").
        target_lang (str): ISO 639-1 code of the target language (default "FR").

    Returns:
        List[Dict]: List of raw translation responses in the same order as input.
    """
    client = DeepL(auth_key=DEEPL_AUTH_KEY)
    results = client.translate_batch(
        texts, source_lang=source_lang, target_lang=target_lang
    )
    return results
