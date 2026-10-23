"""
script_translate.py - Translate narration scripts before synthesis using DeepL.

Provider: DeepL API (https://api.deepl.com)
SDK: deepl Python package
"""

from __future__ import annotations

import os
from typing import List, Optional

import deepl


DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_API_HOST_FREE = "https://api-free.deepl.com"
DEEPL_API_HOST_PRO = "https://api.deepl.com"

# Common target language codes for DeepL
DEEPL_LANG_EN = "EN"
DEEPL_LANG_ES = "ES"
DEEPL_LANG_FR = "FR"
DEEPL_LANG_DE = "DE"
DEEPL_LANG_IT = "IT"
DEEPL_LANG_PT = "PT"
DEEPL_LANG_JA = "JA"
DEEPL_LANG_ZH = "ZH"
DEEPL_LANG_KO = "KO"
DEEPL_LANG_RU = "RU"
DEEPL_LANG_AR = "AR"
DEEPL_LANG_NL = "NL"
DEEPL_LANG_PL = "PL"


def get_deepl_client(
    api_key: Optional[str] = None,
    use_free_api: bool = True,
) -> deepl.Translator:
    """Create a DeepL API client.

    Args:
        api_key: DeepL API key. Falls back to DEEPL_API_KEY env var.
        use_free_api: If True, use api-free.deepl.com endpoint.

    Returns:
        Configured DeepL Translator instance.
    """
    key = api_key or DEEPL_API_KEY
    if not key:
        raise ValueError(
            "DEEPL_API_KEY environment variable must be set "
            "or an explicit api_key must be provided."
        )

    server_url = DEEPL_API_HOST_FREE if use_free_api else DEEPL_API_HOST_PRO
    client = deepl.Translator(key, server_url=server_url)
    return client


def translate_script(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    api_key: Optional[str] = None,
    use_free_api: bool = True,
    formality: Optional[str] = None,
    preserve_formatting: bool = True,
) -> str:
    """Translate a narration script using the DeepL API.

    Supports DeepL's full feature set including formality control
    and formatting preservation.

    Args:
        text: Source text to translate.
        target_lang: Target language code (e.g., 'EN', 'ES', 'JA').
        source_lang: Source language code. Auto-detected if None.
        api_key: Optional explicit API key override.
        use_free_api: Use DeepL free API endpoint.
        formality: 'more' or 'less' formality (for supported languages).
        preserve_formatting: Preserve input formatting in output.

    Returns:
        Translated text string.
    """
    client = get_deepl_client(api_key=api_key, use_free_api=use_free_api)

    kwargs = {}
    if source_lang:
        kwargs["source_lang"] = source_lang
    if formality:
        kwargs["formality"] = formality
    kwargs["preserve_formatting"] = preserve_formatting

    result = client.translate_text(text, target_lang=target_lang, **kwargs)
    return result.text


def translate_script_batch(
    texts: List[str],
    target_lang: str,
    source_lang: Optional[str] = None,
    api_key: Optional[str] = None,
    use_free_api: bool = True,
) -> List[str]:
    """Translate multiple narration scripts using DeepL batch API.

    Args:
        texts: List of source texts to translate.
        target_lang: Target language code.
        source_lang: Source language code (auto-detected if None).
        api_key: Optional explicit API key override.
        use_free_api: Use DeepL free API endpoint.

    Returns:
        List of translated text strings.
    """
    client = get_deepl_client(api_key=api_key, use_free_api=use_free_api)

    kwargs = {}
    if source_lang:
        kwargs["source_lang"] = source_lang

    results = client.translate_text(texts, target_lang=target_lang, **kwargs)
    return [r.text for r in results]


def detect_script_language(text: str, api_key: Optional[str] = None) -> str:
    """Detect the language of a narration script using DeepL.

    Args:
        text: Text to analyze.
        api_key: Optional explicit API key override.

    Returns:
        Detected language code (e.g., 'EN', 'ES').
    """
    client = get_deepl_client(api_key=api_key, use_free_api=True)
    usage = client.get_usage()

    # DeepL SDK auto-detects source language during translation
    # We can use a translate call with no source_lang to detect
    result = client.translate_text(text, target_lang="EN")
    # The detected language is available via the result object
    if hasattr(result, 'detected_source_lang'):
        return result.detected_source_lang
    return "EN"


def get_supported_target_languages(api_key: Optional[str] = None) -> List[dict]:
    """Get list of supported target languages from DeepL.

    Args:
        api_key: Optional explicit API key override.

    Returns:
        List of dicts with 'language' and 'name' keys.
    """
    client = get_deepl_client(api_key=api_key, use_free_api=True)
    languages = client.get_target_languages()
    return [{"language": lang.code, "name": lang.name} for lang in languages]


if __name__ == "__main__":
    sample_text = "Welcome to our presentation on natural language processing."
    translated = translate_script(sample_text, target_lang="ES")
    print(f"Original: {sample_text}")
    print(f"Translated (ES): {translated}")
