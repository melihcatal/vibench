"""
Translate live captions into another language using DeepL API.

Takes streaming transcript text and translates it to the target language
via the DeepL translation service.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

from __future__ import annotations

import asyncio
import os
from typing import AsyncGenerator, Optional

import deepl

# DeepL provider constants
DEEPL_TARGET_LANGUAGE_MAP = {
    "es": "ES",
    "fr": "FR",
    "de": "DE",
    "it": "IT",
    "pt": "PT",
    "ja": "JA",
    "ko": "KO",
    "zh": "ZH",
    "ru": "RU",
    "ar": "AR",
    "nl": "NL",
    "pl": "PL",
    "sv": "SV",
}


def _get_deepl_client(auth_key: Optional[str] = None) -> deepl.Translator:
    """
    Create a DeepL translator client.

    Args:
        auth_key: DeepL API key. Falls back to DEEPL_AUTH_KEY env var.

    Returns:
        Configured deepl.Translator instance.
    """
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise EnvironmentError(
            "DEEPL_AUTH_KEY environment variable must be set or auth_key provided."
        )
    return deepl.Translator(key)


def _resolve_deepl_target_lang(target_lang: str) -> str:
    """
    Resolve a target language code to a DeepL language tag.

    Args:
        target_lang: BCP-47 or short language code (e.g., 'es', 'fr-FR').

    Returns:
        DeepL-compatible language code (uppercase).
    """
    code = target_lang.split("-")[0].upper()
    deepl_code = DEEPL_TARGET_LANGUAGE_MAP.get(target_lang.lower())
    if deepl_code:
        return deepl_code
    return code


async def translate_caption(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> str:
    """
    Translate a single caption text using DeepL API.

    Args:
        text: Source caption text to translate.
        target_language: Target language code (e.g., 'es', 'fr').
        source_language: Optional source language code for auto-detection override.
        auth_key: DeepL API key.

    Returns:
        Translated caption text.
    """
    client = _get_deepl_client(auth_key)
    target_code = _resolve_deepl_target_lang(target_language)

    kwargs = {"target_lang": target_code}
    if source_language:
        source_code = _resolve_deepl_target_lang(source_language)
        kwargs["source_lang"] = source_code

    result = client.translate_text(text, **kwargs)
    return result.text


async def translate_live_captions(
    caption_stream: AsyncGenerator[str, None],
    target_language: str,
    source_language: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> AsyncGenerator[dict, None]:
    """
    Translate a stream of live captions into another language using DeepL API.

    Consumes caption text from an async generator, translates each caption
    via the DeepL translation service, and yields the translated results.

    Args:
        caption_stream: Async generator yielding source-language caption strings.
        target_language: Target language code (e.g., 'es', 'fr', 'ja').
        source_language: Optional source language code.
        auth_key: DeepL API key.

    Yields:
        Dict with keys:
            - 'original': Original caption text
            - 'translated': Translated caption text
            - 'target_language': Target language code
            - 'confidence': Translation confidence (always 1.0 for DeepL)
    """
    client = _get_deepl_client(auth_key)
    target_code = _resolve_deepl_target_lang(target_language)
    source_code = None
    if source_language:
        source_code = _resolve_deepl_target_lang(source_language)

    async for caption in caption_stream:
        if not caption.strip():
            continue

        try:
            kwargs = {"target_lang": target_code}
            if source_code:
                kwargs["source_lang"] = source_code

            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, lambda: client.translate_text(caption, **kwargs)
            )

            yield {
                "original": caption,
                "translated": result.text,
                "target_language": target_language,
                "confidence": 1.0,
            }
        except deepl.DeepLException as e:
            yield {
                "original": caption,
                "translated": "",
                "target_language": target_language,
                "confidence": 0.0,
                "error": str(e),
            }
