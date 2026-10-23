# [SAME-SCENARIO] translate_text.py
"""Translate a single text string between languages using a concrete external provider."""

import os
import json
from typing import Dict, Any

# Import a concrete provider SDK and configure client (e.g., deepl)
import deepl

# Configure client using environment variables (provider-specific)
API_KEY = os.getenv("DEEPL_API_KEY")
translator = deepl.Translator(API_KEY)


def translate_text(source_text: str, target_lang: str, source_lang: str = "EN") -> str:
    """Translate a single text string preserving any markup.

    Args:
        source_text: The text to translate.
        target_lang: Target language code (e.g., "FR").
        source_lang: Source language code (default "EN").

    Returns:
        Translated text string.
    """
    try:
        result = translator.translate_text(
            source_text, target_lang=target_lang, source_lang=source_lang
        )
        return result["text"]
    except Exception as e:
        raise RuntimeError(f"Translation error: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Translate a single text string.")
    parser.add_argument("text", help="The source text to translate.")
    parser.add_argument("target_lang", help="Target language code (e.g., fr).")
    parser.add_argument(
        "source_lang",
        nargs="?",
        default="en",
        help="Source language code (default: en).",
    )
    args = parser.parse_args()
    print(translate_text(args.text, args.target_lang, args.source_lang))
