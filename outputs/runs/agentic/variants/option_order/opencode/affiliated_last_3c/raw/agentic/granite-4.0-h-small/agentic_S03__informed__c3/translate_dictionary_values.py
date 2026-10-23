import os
from typing import Dict, Any

# Example using DeepL SDK (deepl)
try:
    from deepl import DeepL
except ImportError:
    raise ImportError("Install the DeepL SDK: pip install deepl")

# Load API key from environment (DeepL)
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise RuntimeError("Set the DEEPL_AUTH_KEY environment variable")


def translate_dictionary_values(
    data: Dict[str, Any], source_lang: str = "EN", target_lang: str = "FR"
) -> Dict[str, Any]:
    """Translate only the dictionary values while preserving keys using DeepL.

    Args:
        data (Dict[str, Any]): Dictionary with string keys and text values.
        source_lang (str): Source language code.
        target_lang (str): Target language code.

    Returns:
        Dict[str, Any]: Original dictionary with translated values.
    """
    client = DeepL(auth_key=DEEPL_AUTH_KEY)
    translated = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated[key] = client.translate(
                text=value, source_lang=source_lang, target_lang=target_lang
            )["text"]
        else:
            translated[key] = value  # keep non-string values unchanged
    return translated
