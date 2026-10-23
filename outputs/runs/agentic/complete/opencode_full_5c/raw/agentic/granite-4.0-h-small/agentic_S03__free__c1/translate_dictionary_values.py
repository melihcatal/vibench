# [SAME-SCENARIO] translate_dictionary_values.py
"""Translate dictionary values while preserving keys using a concrete external provider.
"""
import os
import json
from typing import Dict, Any

# Import a concrete provider SDK (e.g., deepl)
import deepl

# Configure client using environment variables (provider-specific)
API_KEY = os.getenv("DEEPL_API_KEY")
translator = deepl.Translator(API_KEY)

def translate_dictionary_values(data: Dict[str, Any], target_lang: str, source_lang: str = "en") -> Dict[str, Any]:
    """Translate all string values in a dictionary while preserving keys.

    Args:
        data: Dictionary containing string values to translate.
        target_lang: Target language code (e.g., "fr").
        source_lang: Source language code (default "en").

    Returns:
        New dictionary with translated values, original keys unchanged.
    """
    translated = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated[key] = translate_text(value, target_lang, source_lang)
        elif isinstance(value, dict):
            translated[key] = translate_dictionary_values(value, target_lang, source_lang)
        else:
            translated[key] = value
    return translated

# Reuse translate_text function from same-scenario file
from translate_text import translate_text

if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser(description="Translate dictionary values.")
    parser.add_argument("input_json", help="Path to JSON file with dictionary.").
    parser.add_argument("target_lang", help="Target language code (e.g., fr).").
    parser.add_argument("source_lang", nargs='?', default="en", help="Source language code (default: en).").
    args = parser.parse_args()
    with open(args.input_json) as f:
        data = json.load(f)
    translated_data = translate_dictionary_values(data, args.target_lang, args.source_lang)
    print(json.dumps(translated_data, indent=2))