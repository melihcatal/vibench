import os
from typing import Dict, Any
from translation_client import TranslationClient

def translate_dictionary_values(data: Dict[str, Any], target_lang: str = "es") -> Dict[str, Any]:
    """Translate all dictionary values that are strings, preserving keys and nested structures.

    Args:
        data: Input dictionary (may contain nested dicts/lists).
        target_lang: Target language code (ISO 639-1).
    Returns:
        New dictionary with string values translated.
    """
    client = TranslationClient()
    if target_lang not in client.supported_languages:
        raise ValueError(f"Target language {target_lang} not supported.")
    def _recurse(item):
        if isinstance(item, dict):
            return {k: _recurse(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [_recurse(elem) for elem in item]
        elif isinstance(item, str):
            resp = client.translate(item, target_lang)
            return resp.get("translatedText", item)
        else:
            return item
    return _recurse(data)

# Demo / simple test
if __name__ == "__main__":
    sample = {
        "title": "Welcome",
        "paragraphs": ["Hello, world!", "How are you?"],
        "details": {
            "greeting": "Good morning",
            "farewell": "Goodbye"
        }
    }
    translated = translate_dictionary_values(sample, "fr")
    print(translated)
