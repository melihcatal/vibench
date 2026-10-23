"""
Local configuration and client helper utilities for General Text Translation.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

import os
from typing import List, Optional

import deepl

from translation_models import (
    TranslationRequest,
    TranslationResult,
    TranslationResponse,
    build_translation_request,
    parse_translation_response,
    validate_language_pair,
)


class DeepLTranslationClient:
    """Client wrapper around the DeepL Translation API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("DEEPL_AUTH_KEY", "")
        if not self.api_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable is required for DeepL API access.")
        self._client = deepl.Translator(self.api_key)

    @property
    def client(self) -> deepl.Translator:
        return self._client

    def translate(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None,
        formality: Optional[str] = None,
        tag_handling: Optional[str] = None,
        ignore_tags: Optional[List[str]] = None,
        preserve_formatting: bool = True,
    ) -> TranslationResult:
        """Translate a single text string."""
        if not validate_language_pair(source_lang, target_lang):
            raise ValueError(
                f"Invalid language pair: source={source_lang}, target={target_lang}"
            )

        kwargs = {}
        if source_lang:
            kwargs["source_lang"] = source_lang.upper()
        if formality:
            kwargs["formality"] = formality
        if tag_handling:
            kwargs["tag_handling"] = tag_handling
        if ignore_tags:
            kwargs["ignore_tags"] = ignore_tags
        if preserve_formatting:
            kwargs["preserve_formatting"] = True

        result = self._client.translate_text(text, target_lang=target_lang.upper(), **kwargs)

        billing_chars = len(result.text)
        return TranslationResult(
            text=result.text,
            source_lang=source_lang or result.detected_source_lang or "auto",
            target_lang=target_lang.upper(),
            detected_source_lang=result.detected_source_lang,
            billing_chars=billing_chars,
        )

    def translate_batch(
        self,
        texts: List[str],
        target_lang: str,
        source_lang: Optional[str] = None,
        formality: Optional[str] = None,
        tag_handling: Optional[str] = None,
        ignore_tags: Optional[List[str]] = None,
        preserve_formatting: bool = True,
    ) -> TranslationResponse:
        """Translate a list of texts in a single API call, preserving order."""
        if not validate_language_pair(source_lang, target_lang):
            raise ValueError(
                f"Invalid language pair: source={source_lang}, target={target_lang}"
            )

        kwargs = {}
        if source_lang:
            kwargs["source_lang"] = source_lang.upper()
        if formality:
            kwargs["formality"] = formality
        if tag_handling:
            kwargs["tag_handling"] = tag_handling
        if ignore_tags:
            kwargs["ignore_tags"] = ignore_tags
        if preserve_formatting:
            kwargs["preserve_formatting"] = True

        results = self._client.translate_text(texts, target_lang=target_lang.upper(), **kwargs)

        response = TranslationResponse()
        for res in results:
            billing_chars = len(res.text)
            tr = TranslationResult(
                text=res.text,
                source_lang=source_lang or res.detected_source_lang or "auto",
                target_lang=target_lang.upper(),
                detected_source_lang=res.detected_source_lang,
                billing_chars=billing_chars,
            )
            response.add_result(tr)

        return response

    def translate_with_request(self, request: TranslationRequest) -> TranslationResult:
        """Translate using a TranslationRequest object."""
        return self.translate(
            text=request.text,
            target_lang=request.target_lang,
            source_lang=request.source_lang,
            formality=request.formality,
            tag_handling=request.tag_handling,
            ignore_tags=request.ignore_tags,
            preserve_formatting=request.preserve_formatting,
        )

    def translate_multiple_requests(
        self, requests: List[TranslationRequest]
    ) -> TranslationResponse:
        """Translate multiple TranslationRequest objects in batch."""
        if not requests:
            return TranslationResponse()

        texts = [r.text for r in requests]
        batch_result = self.translate_batch(
            texts=texts,
            target_lang=requests[0].target_lang,
            source_lang=requests[0].source_lang,
            formality=requests[0].formality,
            tag_handling=requests[0].tag_handling,
            ignore_tags=requests[0].ignore_tags,
            preserve_formatting=requests[0].preserve_formatting,
        )
        return batch_result


def get_client() -> DeepLTranslationClient:
    """Factory function to create a configured DeepL translation client."""
    return DeepLTranslationClient()
