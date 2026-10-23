# Python code for translate_text.py
import os
import json
from typing import Dict, Optional

from translation_client import GeneralTextTranslationClient


def translate_text(
    source_text: str,
    source_lang: str = "en",
    target_lang: str = "zh",
    **kwargs,
) -> Dict:
    """Translate a single text string using a configured translation client.

    Args:
        source_text (str): The source text to translate.
        source_lang (str): Source language code.
        target_lang (str): Target language code.
        **kwargs: Additional provider-specific arguments.

    Returns:
        Dict: The translation result as provided by the underlying provider.
    """
    client = GeneralTextTranslationClient()
    result = client.translate(
        texts=[source_text],
        source_lang=source_lang,
        target_lang=target_lang,
        **kwargs,
    )
    return result[0]
