# [SAME-SCENARIO] batch_translate.py
"""Translate a list of text strings while preserving order using a concrete external provider.
"""
import os
import json
from typing import List

# Import a concrete provider SDK and configure client (e.g., googlecloudtranslate)
from google.cloud import translate_v2 as translate

# Configure client using environment variables (provider-specific)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
translator = translate.Client()

def batch_translate(texts: List[str], target_lang: str, source_lang: str = "en") -> List[str]:
    """Translate a list of texts preserving original ordering.

    Args:
        texts: List of source texts.
        target_lang: Target language code (e.g., "es").
        source_lang: Source language code (default "en").

    Returns:
        List of translated texts in the same order as input.
    """
    try:
        result = translator.translate(texts, source_language=source_lang, target_language=target_lang)
        # result is a list of dicts with 'translatedText'
        return [item['translatedText'] for item in result]
    except Exception as e:
        raise RuntimeError(f"Batch translation error: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Batch translate texts.")
    parser.add_argument("texts", nargs='+', help="One or more source texts to translate.")
    parser.add_argument("target_lang", help="Target language code (e.g., es).").
    parser.add_argument("source_lang", nargs='?', default="en", help="Source language code (default: en).")
    args = parser.parse_args()
    translations = batch_translate(args.texts, args.target_lang, args.source_lang)
    for t in translations:
        print(t)