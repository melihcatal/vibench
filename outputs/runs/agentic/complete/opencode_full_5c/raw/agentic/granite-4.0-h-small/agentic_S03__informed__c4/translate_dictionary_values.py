"""Translate dictionary values while preserving keys."""

from translation_client import build_client
from translation_models import (
    normalize_translate_text_payload,
    parse_translate_text_response,
)
from typing import Dict, Any

# Provider identifiers (choose one concrete service)
PROVIDER_NAME = "Google Cloud Translation"  # <provider>
PROVIDER_SDK = "google-cloud-translate"


def translate_dict_values(
    source: Dict[str, str], target_lang: str = "en"
) -> Dict[str, str]:
    """Translate string values in a dictionary, keeping keys unchanged.

    Parameters:
        source: dictionary whose values are strings to translate.
        target_lang: ISO language code of destination.
    Returns:
        New dictionary with translated values.
    """
    client = build_client()
    translated = {}
    for key, text in source.items():
        payload = normalize_translate_text_payload(text, target_lang)
        raw_resp = client.translate(text, target_language=target_lang)
        translated[key] = parse_translate_text_response(raw_resp)
    return translated


# Simple demo if run directly
if __name__ == "__main__":
    demo_dict = {"greeting": "Hello", "farewell": "Goodbye"}
    print("Source:", demo_dict)
    print("Translated:", translate_dict_values(demo_dict, target_lang="fr"))
