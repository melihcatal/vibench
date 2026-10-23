# Python code for batch_translate.py
import os
import json
from typing import List, Dict

from translation_client import GeneralTextTranslationClient


def batch_translate(
    texts: List[str],
    source_lang: str = "en",
    target_lang: str = "zh",
    **kwargs,
) -> List[Dict]:
    """Translate a list of text strings while preserving order.

    Args:
        texts (List[str]): List of source texts.
        source_lang (str): Source language code.
        target_lang (str): Target language code.
        **kwargs: Additional provider-specific arguments.

    Returns:
        List[Dict]: List of translation results.
    """
    client = GeneralTextTranslationClient()
    results = client.translate(
        texts=texts,
        source_lang=source_lang,
        target_lang=target_lang,
        **kwargs,
    )
    return results
