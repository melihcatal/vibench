# [HELPER] translation_client.py
"""Local configuration and client helper utilities for General Text Translation.
This file loads provider credentials, initializes provider-specific clients,
and provides a thin wrapper for common translate operations."

import os
import json
from typing import Any, Dict, Optional

# Concrete provider SDKs (choose one per scenario)
# Example: deepl for simple string translation
try:
    import deepl
except ImportError:
    deepl = None

# Example: google cloud translate for markup preservation
try:
    from google.cloud import translate_v2 as translate
except ImportError:
    translate = None

# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

def load_credentials() -> Dict[str, Optional[str]]:
    """Load provider API keys/secrets from environment variables or local config files.
    Returns a dict with concrete provider keys."
    creds = {
        "deepl_api_key": os.getenv("DEEPL_API_KEY"),
        "google_application_credentials": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    }
    # Optionally load a local JSON config if present
    config_path = os.path.join(os.getcwd(), "translation_credentials.json")
    if os.path.exists(config_path):
        with open(config_path) as f:
            extras = json.load(f)
            creds.update(extras)
    return creds

# ---------------------------------------------------------------------------
# Client factories
# ---------------------------------------------------------------------------

def get_deepl_client() -> deepl.Translator:
    """Return a configured deepl.Translator instance.
    Raises RuntimeError if API key is missing.
    """
    api_key = load_credentials()["deepl_api_key"]
    if not api_key:
        raise RuntimeError("Missing DEEPL_API_KEY environment variable.")
    return deepl.Translator(api_key)


def get_google_translate_client() -> translate.Client:
    """Return a configured google.cloud.translate.Client instance.
    Uses GOOGLE_APPLICATION_CREDENTIALS env var for credentials.
    """
    creds_path = load_credentials()["google_application_credentials"]
    if creds_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
    return translate.Client()

# ---------------------------------------------------------------------------
# Common wrapper utilities
# ---------------------------------------------------------------------------

def translate_text_provider(source_text: str, target_lang: str, source_lang: str = "en", provider: str = "deepl") -> str:
    """Generic wrapper that dispatches to the chosen concrete provider.

    Args:
        source_text: Text to translate.
        target_lang: Target language code.
        source_lang: Source language code (default "en").
        provider: Identifier {'deepl', 'google'}.

    Returns:
        Translated text string.
    """
    if provider == "deepl":
        client = get_deepl_client()
        result = client.translate_text(source_text, target_lang=target_lang, source_lang=source_lang)
        return result["text"]
    elif provider == "google":
        client = get_google_translate_client()
        result = client.translate(source_text, target_language=target_lang, source_language=source_lang, format_='html')
        return result['translatedText']
    else:
        raise ValueError(f"Unsupported provider: {provider}")

# ---------------------------------------------------------------------------
# Example usage (when executed directly)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Utility to translate text using selected provider.")
    parser.add_argument("source_text", help="Text to translate.")
    parser.add_argument("target_lang", help="Target language code.")
    parser.add_argument("provider", choices=["deepl", "google"], help="Provider to use.")
    parser.add_argument("--source_lang", default="en", help="Source language (default: en).")
    args = parser.parse_args()
    print(translate_text_provider(args.source_text, args.target_lang, args.source_lang, args.provider))