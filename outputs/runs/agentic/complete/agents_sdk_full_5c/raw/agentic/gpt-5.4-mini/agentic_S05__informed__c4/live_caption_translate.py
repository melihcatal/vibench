from __future__ import annotations

from typing import Iterable, List, Optional

import deepl

from speech_models import CaptionRequest, normalize_transcript_text

DEFAULT_TARGET_LANGUAGE = deepl.Language.ENGLISH


class LiveCaptionTranslator:
    def __init__(self, auth_key: Optional[str] = None) -> None:
        self.auth_key = auth_key or __import__("os").getenv("DEEPL_AUTH_KEY", "")
        self.translator = deepl.Translator(self.auth_key) if self.auth_key else None

    def translate_chunk(self, text: str, target_language: str = DEFAULT_TARGET_LANGUAGE) -> str:
        if self.translator is None:
            raise RuntimeError("DEEPL_AUTH_KEY is required")
        result = self.translator.translate_text(normalize_transcript_text(text), target_lang=target_language)
        return result.text


def translate_live_captions(chunks: Iterable[str], request: CaptionRequest, auth_key: Optional[str] = None) -> List[str]:
    translator = LiveCaptionTranslator(auth_key)
    target = request.target_language or DEFAULT_TARGET_LANGUAGE
    return [translator.translate_chunk(chunk, target_language=target) for chunk in chunks if normalize_transcript_text(chunk)]
