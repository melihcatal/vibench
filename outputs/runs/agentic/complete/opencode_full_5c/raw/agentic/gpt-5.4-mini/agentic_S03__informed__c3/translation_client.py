import os
from typing import Optional

import deepl

from translation_models import normalize_mapping_values, normalize_text, normalize_texts


class TranslationClient:
    def __init__(self, auth_key: Optional[str] = None):
        self.auth_key = auth_key or os.environ.get("DEEPL_AUTH_KEY", "")
        if not self.auth_key:
            raise RuntimeError("DEEPL_AUTH_KEY is required")
        self.client = deepl.Translator(self.auth_key)

    def translate_text(self, text: str, source_language: Optional[str] = None, target_language: Optional[str] = None) -> str:
        result = self.client.translate_text(
            normalize_text(text),
            source_lang=source_language,
            target_lang=target_language or "EN-US",
        )
        return str(result)

    def translate_texts(self, texts, source_language: Optional[str] = None, target_language: Optional[str] = None):
        return [self.translate_text(text, source_language, target_language) for text in normalize_texts(texts)]

    def translate_mapping_values(self, values, source_language: Optional[str] = None, target_language: Optional[str] = None):
        normalized = normalize_mapping_values(values)
        return {key: self.translate_text(value, source_language, target_language) for key, value in normalized.items()}

    def translate_html(self, html: str, source_language: Optional[str] = None, target_language: Optional[str] = None) -> str:
        result = self.client.translate_text(
            normalize_text(html),
            source_lang=source_language,
            target_lang=target_language or "EN-US",
            tag_handling="html",
        )
        return str(result)
