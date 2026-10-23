from __future__ import annotations

import os

import deepl


class LiveCaptionTranslator:
    def __init__(self, target_language: str) -> None:
        auth_key = os.getenv("DEEPL_AUTH_KEY")
        if not auth_key:
            raise RuntimeError("DEEPL_AUTH_KEY is required")
        self.client = deepl.Translator(auth_key)
        self.target_language = target_language

    def translate_text(self, text: str, source_language: str | None = None) -> str:
        if not text.strip():
            return ""
        result = self.client.translate_text(
            text,
            target_lang=self.target_language,
            source_lang=source_language,
            model_type="prefer_quality_optimized",
        )
        return result.text
