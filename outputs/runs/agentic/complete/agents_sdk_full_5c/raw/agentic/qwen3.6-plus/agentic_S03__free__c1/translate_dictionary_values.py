"""Translate dictionary values while preserving keys using Azure Translator."""

import os
import json
import requests
from typing import Dict, Any
from translation_client import load_translation_config
from translation_models import TranslationRequest, TranslationResponse, normalize_language_code


AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"
AZURE_TRANSLATOR_API_VERSION = "3.0"


def translate_dictionary_values(
    data: Dict[str, Any],
    source_lang: str,
    target_lang: str,
    value_types: tuple = (str,),
) -> Dict[str, Any]:
    """Translate string values in a dictionary while preserving keys using Azure Translator.

    Args:
        data: Dictionary with translatable string values.
        source_lang: Source language code.
        target_lang: Target language code.
        value_types: Tuple of value types to translate (default: str only).

    Returns:
        Dictionary with translated string values and preserved keys.
    """
    config = load_translation_config()
    azure_key = os.environ.get("AZURE_TRANSLATOR_KEY", config.get("azure_translator_key"))
    azure_region = os.environ.get("AZURE_TRANSLATOR_REGION", config.get("azure_region", "global"))

    if not azure_key:
        raise ValueError("AZURE_TRANSLATOR_KEY environment variable or config is required")

    normalized_source = normalize_language_code(source_lang)
    normalized_target = normalize_language_code(target_lang)

    text_values = [v for v in data.values() if isinstance(v, str)]

    if not text_values:
        return data.copy()

    headers = {
        "Ocp-Apim-Subscription-Key": azure_key,
        "Ocp-Apim-Subscription-Region": azure_region,
        "Content-Type": "application/json",
    }

    params = {
        "api-version": AZURE_TRANSLATOR_API_VERSION,
        "from": normalized_source if normalized_source != "auto" else None,
        "to": normalized_target,
    }

    body = [{"text": text} for text in text_values]

    response = requests.post(
        f"{AZURE_TRANSLATOR_ENDPOINT}/translate",
        headers=headers,
        params={k: v for k, v in params.items() if v is not None},
        json=body,
    )
    response.raise_for_status()

    translation_results = response.json()
    translated_values = [result["translations"][0]["text"] for result in translation_results]

    translated_dict = {}
    val_idx = 0
    for key, value in data.items():
        if isinstance(value, str):
            translated_dict[key] = translated_values[val_idx]
            val_idx += 1
        else:
            translated_dict[key] = value

    return translated_dict


def translate_nested_dictionary(
    data: Dict[str, Any],
    source_lang: str,
    target_lang: str,
) -> Dict[str, Any]:
    """Recursively translate string values in nested dictionaries.

    Args:
        data: Nested dictionary structure.
        source_lang: Source language code.
        target_lang: Target language code.

    Returns:
        Nested dictionary with all string values translated.
    """
    if isinstance(data, dict):
        return translate_dictionary_values(
            {k: translate_nested_dictionary(v, source_lang, target_lang) if isinstance(v, dict) else v
             for k, v in data.items()},
            source_lang,
            target_lang,
        )
    elif isinstance(data, list):
        return [translate_nested_dictionary(item, source_lang, target_lang) for item in data]
    else:
        return data


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 4:
        src = sys.argv[1]
        tgt = sys.argv[2]
        data = json.loads(sys.argv[3])
        result = translate_dictionary_values(data, src, tgt)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Usage: translate_dictionary_values.py <source_lang> <target_lang> <json_dict>")
