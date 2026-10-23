from __future__ import annotations

import os

import deepl

from speech_models import normalize_caption_chunk


def translate_live_caption(text: str, *, target_language: str) -> str:
    normalized = normalize_caption_chunk(text)
    if not normalized:
        return ""
    client = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = client.translate_text(normalized, target_lang=target_language)
    return result.text
