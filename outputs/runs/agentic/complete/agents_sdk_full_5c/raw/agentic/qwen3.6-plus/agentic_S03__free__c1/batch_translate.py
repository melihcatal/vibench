"""Translate a list of strings while preserving order using DeepL API."""

import os
import deepl
from typing import List
from translation_client import load_translation_config
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    normalize_language_code,
)


def batch_translate(
    texts: List[str],
    source_lang: str,
    target_lang: str,
    preserve_formatting: bool = True,
) -> List[TranslationResponse]:
    """Translate a list of strings using DeepL Translator API, preserving order.

    Args:
        texts: List of text strings to translate.
        source_lang: Source language code (e.g., 'EN', 'FR', 'JA').
        target_lang: Target language code.
        preserve_formatting: Whether to preserve original formatting.

    Returns:
        List of TranslationResponse objects in the same order as input.
    """
    config = load_translation_config()
    deepl_api_key = os.environ.get("DEEPL_API_KEY", config.get("deepl_api_key"))

    if not deepl_api_key:
        raise ValueError("DEEPL_API_KEY environment variable or config is required for DeepL API")

    client = deepl.Translator(deepl_api_key)

    normalized_source = normalize_language_code(source_lang).upper()
    normalized_target = normalize_language_code(target_lang).upper()

    # Map common language codes to DeepL format
    lang_map = {"en": "EN", "fr": "FR", "de": "DE", "es": "ES", "ja": "JA", "zh": "ZH"}
    source_code = lang_map.get(normalized_source.lower(), normalized_source)
    target_code = lang_map.get(normalized_target.lower(), normalized_target)

    requests = [
        TranslationRequest(
            text=text,
            source_lang=source_code if source_code != "AUTO" else None,
            target_lang=target_code,
            model="deepl",
        )
        for text in texts
    ]

    source_param = None if source_code == "AUTO" else source_code

    results = client.translate_text(
        texts,
        target_lang=target_code,
        source_lang=source_param,
        preserve_formatting=preserve_formatting,
    )

    responses = []
    for i, result in enumerate(results):
        response = TranslationResponse(
            translated_text=result.text,
            source_lang=result.detected_source_lang if hasattr(result, 'detected_source_lang') else source_code,
            target_lang=target_code,
            model_used="deepl-free" if "api-free.deepl.com" in str(client.server_url) else "deepl-pro",
            confidence=1.0,
            character_count=len(requests[i].text),
        )
        responses.append(response)

    return responses


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) >= 4:
        src = sys.argv[1]
        tgt = sys.argv[2]
        texts = sys.argv[3:]
        results = batch_translate(texts, src, tgt)
        for r in results:
            print(json.dumps(r.to_dict(), ensure_ascii=False))
    else:
        print("Usage: batch_translate.py <source_lang> <target_lang> <text1> [text2] ...")
