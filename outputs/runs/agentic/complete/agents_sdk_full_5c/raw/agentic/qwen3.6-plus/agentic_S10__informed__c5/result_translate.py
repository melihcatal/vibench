"""
Later-step: Translate generated model output.

Provider: DeepL API
SDK: requests (REST API)
Auth: DEEPL_AUTH_KEY
"""

import os
from typing import Optional, Dict, Any, List

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_URL_PRO = "https://api.deepl.com/v2/translate"


def _get_deepl_config() -> Dict[str, str]:
    """
    Retrieve DeepL API configuration from environment.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")
    return {"auth_key": auth_key}


def translate_text(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
    preserve_formatting: bool = True,
) -> Dict[str, Any]:
    """
    Translate text using the DeepL Translation API.

    Args:
        text: The source text to translate.
        target_lang: Target language code (e.g., "ES", "FR", "DE", "JA", "ZH").
        source_lang: Optional source language code. If None, DeepL auto-detects.
        formality: Optional formality level ("more", "less", "default", "prefer_more", "prefer_less").
        preserve_formatting: Whether to preserve XML/HTML formatting in the text.

    Returns:
        A dict containing the translated text and metadata.
    """
    config = _get_deepl_config()

    # Choose free or pro endpoint based on key suffix
    api_url = DEEPL_API_URL
    if config["auth_key"].endswith(":fx"):
        api_url = DEEPL_API_URL_PRO

    payload: Dict[str, Any] = {
        "text": text,
        "target_lang": target_lang.upper(),
    }

    if source_lang:
        payload["source_lang"] = source_lang.upper()

    if formality:
        payload["formality"] = formality

    if preserve_formatting:
        payload["preserve_formatting"] = True

    headers = {
        "Authorization": f"DeepL-Auth-Key {config['auth_key']}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(api_url, headers=headers, data=payload, timeout=30)
    response.raise_for_status()
    data = response.json()

    translations = data.get("translations", [])
    if not translations:
        raise ValueError("DeepL API returned no translations.")

    translated_texts = [t.get("text", "") for t in translations]
    detected_lang = translations[0].get("detected_source_language", "")

    return {
        "translated_text": " ".join(translated_texts) if len(translated_texts) == 1 else translated_texts,
        "source_language": source_lang or detected_lang,
        "target_language": target_lang.upper(),
        "raw_response": data,
    }


def translate_to_multiple(
    text: str,
    target_langs: List[str],
    source_lang: Optional[str] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Translate text into multiple target languages via DeepL.

    Args:
        text: The source text.
        target_langs: List of target language codes.
        source_lang: Optional source language code.

    Returns:
        A dict mapping each target language to its translation result.
    """
    results = {}
    for lang in target_langs:
        results[lang.upper()] = translate_text(
            text=text,
            target_lang=lang,
            source_lang=source_lang,
        )
    return results


def detect_language(text: str) -> str:
    """
    Detect the source language of text using DeepL.

    Args:
        text: The text to analyze.

    Returns:
        The detected language code.
    """
    result = translate_text(text, target_lang="EN")
    return result.get("source_language", "UNKNOWN")
