"""
translation_client.py - Provide local configuration and client helper utilities
for General Text Translation using DeepL API.
"""

import os
from typing import Any, Dict, List, Optional

import deepl

from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResponse,
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
    TranslationRequest,
    TranslationResponse,
    normalize_source_lang,
    normalize_target_lang,
)


class TranslationClient:
    """Client wrapper around the DeepL Translation API."""

    def __init__(self, auth_key: Optional[str] = None, server_url: Optional[str] = None):
        self.auth_key = auth_key or os.environ.get("DEEPL_AUTH_KEY", "")
        if not self.auth_key:
            raise ValueError(
                "DEEPL_AUTH_KEY environment variable or auth_key parameter is required "
                "for DeepL API access."
            )
        if server_url:
            self.client = deepl.Translator(self.auth_key, server_url=server_url)
        else:
            self.client = deepl.Translator(self.auth_key)

    def translate(
        self,
        text: str,
        source_lang: Optional[str] = None,
        target_lang: str = "en",
        preserve_formatting: bool = True,
        formal: bool = False,
    ) -> TranslationResponse:
        """Translate a single text string using DeepL."""
        source = normalize_source_lang(source_lang)
        target = normalize_target_lang(target_lang)

        kwargs: Dict[str, Any] = {
            "target_lang": target,
            "preserve_formatting": preserve_formatting,
        }
        if source:
            kwargs["source_lang"] = source
        if formal:
            kwargs["formality"] = "prefer_more"

        result = self.client.translate_text(text, **kwargs)

        return TranslationResponse(
            translated_text=result.text,
            source_lang=result.detected_source_lang if source is None else (source or ""),
            target_lang=target,
            detected_source=(source is None),
            character_count=len(text),
            billing_characters=result.billed_characters,
        )

    def batch_translate(
        self,
        texts: List[str],
        source_lang: Optional[str] = None,
        target_lang: str = "en",
        preserve_formatting: bool = True,
    ) -> BatchTranslationResponse:
        """Translate a list of strings using DeepL, preserving order."""
        source = normalize_source_lang(source_lang)
        target = normalize_target_lang(target_lang)

        kwargs: Dict[str, Any] = {
            "target_lang": target,
            "preserve_formatting": preserve_formatting,
        }
        if source:
            kwargs["source_lang"] = source

        results = self.client.translate_text(texts, **kwargs)

        translated = [r.text for r in results]
        total_chars = sum(len(t) for t in texts)

        return BatchTranslationResponse(
            translations=translated,
            source_lang=source or "",
            target_lang=target,
            total_characters=total_chars,
        )

    def translate_dict_values(
        self,
        data: Dict[str, Any],
        source_lang: Optional[str] = None,
        target_lang: str = "en",
        keys_to_skip: Optional[List[str]] = None,
    ) -> DictionaryTranslationResponse:
        """Translate dictionary values while preserving keys."""
        keys_to_skip = keys_to_skip or []
        source = normalize_source_lang(source_lang)
        target = normalize_target_lang(target_lang)

        texts_to_translate = []
        keys_to_translate = []

        for key, value in data.items():
            if key in keys_to_skip:
                continue
            if isinstance(value, str):
                texts_to_translate.append(value)
                keys_to_translate.append(key)

        if not texts_to_translate:
            return DictionaryTranslationResponse(
                translated_data=dict(data),
                source_lang=source or "",
                target_lang=target,
                translated_keys=[],
            )

        kwargs: Dict[str, Any] = {
            "target_lang": target,
        }
        if source:
            kwargs["source_lang"] = source

        results = self.client.translate_text(texts_to_translate, **kwargs)

        translated_data = dict(data)
        translated_keys = []
        for i, key in enumerate(keys_to_translate):
            translated_data[key] = results[i].text
            translated_keys.append(key)

        return DictionaryTranslationResponse(
            translated_data=translated_data,
            source_lang=source or "",
            target_lang=target,
            translated_keys=translated_keys,
        )

    def translate_html_segments(
        self,
        segments: List[str],
        source_lang: Optional[str] = None,
        target_lang: str = "en",
    ) -> List[str]:
        """Translate a list of text segments (used for markup translation)."""
        source = normalize_source_lang(source_lang)
        target = normalize_target_lang(target_lang)

        if not segments:
            return []

        kwargs: Dict[str, Any] = {
            "target_lang": target,
            "tag_handling": "html",
            "preserve_formatting": True,
        }
        if source:
            kwargs["source_lang"] = source

        results = self.client.translate_text(segments, **kwargs)
        return [r.text for r in results]
