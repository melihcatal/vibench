from __future__ import annotations

import os

import deepl

from speech_models import CaptionChunk, merge_caption_chunks


DEEPL_ENV = "DEEPL_AUTH_KEY"


def translate_live_captions(chunks: list[CaptionChunk], target_language: str) -> str:
    auth_key = os.getenv(DEEPL_ENV)
    if not auth_key:
        raise RuntimeError(f"Missing required environment variable: {DEEPL_ENV}")
    client = deepl.Translator(auth_key)
    source_text = merge_caption_chunks(chunks)
    result = client.translate_text(source_text, target_lang=target_language)
    return result.text
