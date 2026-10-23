"""Translates a list of strings while preserving order."""

from translation_client import build_client
from translation_models import (
    normalize_translate_text_payload,
    parse_translate_text_response,
)
from typing import List, Dict, Any

# Provider identifiers (choose one concrete service)
PROVIDER_NAME = "Google Cloud Translation"  # <provider>
PROVIDER_SDK = "google-cloud-translate"


def translate_batch(texts: List[str], target_lang: str = "en") -> List[str]:
    """Translate multiple strings, preserving the input order.

    Parameters:
        texts: sequence of source strings.
        target_lang: ISO language code of the destination.
    Returns:
        List of translated strings, aligned with the input list.
    """
    client = build_client()
    # Google Cloud Translation SDK supports batch translation via the ``translate_text`` method
    # with ``client.translate()`` called in a loop, preserving order.
    results = []
    for text in texts:
        payload = normalize_translate_text_payload(text, target_lang)
        # low-level SDK call (same as single‑string helper but invoked per item)
        raw_resp = client.translate(text, target_language=target_lang)
        results.append(parse_translate_text_response(raw_resp))
    return results
