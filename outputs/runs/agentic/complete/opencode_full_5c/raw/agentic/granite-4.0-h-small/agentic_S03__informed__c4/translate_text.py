"""Translates a single text string between languages."""

from translation_client import build_client, translate_text
from translation_models import (
    normalize_translate_text_payload,
    parse_translate_text_response,
)

# Provider identifiers (choose one concrete service)
PROVIDER_NAME = "Google Cloud Translation"  # <provider>
PROVIDER_SDK = "google-cloud-translate"


def translate_string(text: str, target_lang: str = "en") -> str:
    """Translate *one* string to the requested target language.

    Parameters:
        text: source text.
        target_lang: ISO language code of the destination.
    Returns:
        Translated text.
    """
    # 1. build client (handles creds and service init)
    client = build_client()
    # 2. normalize request payload
    payload = normalize_translate_text_payload(text, target_lang)
    # 3. call the provider
    raw_resp = client.translate(text, target_language=target_lang)
    # 4. parse response
    result = parse_translate_text_response(raw_resp)
    return result
