from __future__ import annotations

import os
from typing import Iterable, List, Optional

import deepl

from translation_models import (
    BatchTranslationResult,
    TranslationResult,
    normalize_language_code,
)


DEEPL_API_URL = "https://api.deepl.com"


def get_translator() -> deepl.Translator:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    server_url = os.getenv("DEEPL_SERVER_URL", DEEPL_API_URL)
    return deepl.Translator(auth_key=auth_key, server_url=server_url)


def translate_text_items(
    texts: Iterable[str],
    target_language: str,
    source_language: Optional[str] = None,
    tag_handling: Optional[str] = None,
) -> BatchTranslationResult:
    translator = get_translator()
    items = list(texts)
    response = translator.translate_text(
        items,
        target_lang=normalize_language_code(target_language),
        source_lang=normalize_language_code(source_language),
        tag_handling=tag_handling,
    )
    results: List[TranslationResult] = []
    for entry in response:
        results.append(
            TranslationResult(
                text=entry.text,
                detected_source_language=getattr(entry, "detected_source_lang", None),
                provider="DeepL",
                raw={
                    "billed_characters": getattr(entry, "billed_characters", None),
                    "model_type_used": getattr(entry, "model_type_used", None),
                },
            )
        )
    return BatchTranslationResult(
        translations=results, provider="DeepL", raw={"count": len(results)}
    )
