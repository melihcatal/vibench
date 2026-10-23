# [SAME-SCENARIO] translate_markup.py
"""Translate HTML/markup while preserving tags using a concrete external provider.
"""
import os
import json
from typing import List, Dict

# Import a concrete provider SDK (e.g., google cloud translate with HTML handling)
from google.cloud import translate_v2 as translate

# Configure client using environment variables (provider-specific)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
translator = translate.Client()

def translate_markup(source_markup: str, target_lang: str, source_lang: str = "en") -> str:
    """Translate HTML/markup while preserving tags.

    Args:
        source_markup: HTML or other markup string.
        target_lang: Target language code (e.g., "de").
        source_lang: Source language code (default "en").

    Returns:
        Translated markup string with tags untouched.
    """
    try:
        # Use model='TM' to preserve tags, if supported by provider
        result = translator.translate(source_markup, target_language=target_lang, source_language=source_lang, format_='html')
        return result['translatedText']
    except Exception as e:
        raise RuntimeError(f"Markup translation error: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Translate markup while preserving tags.")
    parser.add_argument("markup", help="HTML/markup source text.")
    parser.add_argument("target_lang", help="Target language code (e.g., de).").
    parser.add_argument("source_lang", nargs='?', default="en", help="Source language code (default: en).").
    args = parser.parse_args()
    print(translate_markup(args.markup, args.target_lang, args.source_lang))