"""
Translate live captions into another language using DeepL API.
Takes streaming transcript text and translates it in real-time for live captioning.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

import logging
from typing import Optional

import deepl

from speech_models import FinalTranscriptResult

logger = logging.getLogger(__name__)

# DeepL supported target language codes
DEEPL_LANGUAGE_MAP = {
    "en": "EN",
    "es": "ES",
    "fr": "FR",
    "de": "DE",
    "it": "IT",
    "pt": "PT",
    "nl": "NL",
    "pl": "PL",
    "ru": "RU",
    "ja": "JA",
    "zh": "ZH",
    "ko": "KO",
}


class LiveCaptionTranslator:
    """
    Translates live caption text using the DeepL Translation API.

    Provides streaming translation of transcript chunks with configurable
    source and target languages.
    """

    def __init__(
        self,
        target_language: str = "es",
        source_language: Optional[str] = None,
        api_key: Optional[str] = None,
        formal: bool = True,
    ):
        """
        Initialize the DeepL caption translator.

        Args:
            target_language: Target language code (e.g., 'es' for Spanish).
            source_language: Source language code (None for auto-detect).
            api_key: DeepL API key. Falls back to DEEPL_AUTH_KEY env var.
            formal: Whether to use formal tone (DeepL feature).
        """
        self.target_language = DEEPL_LANGUAGE_MAP.get(target_language, target_language.upper())
        self.source_language = DEEPL_LANGUAGE_MAP.get(source_language, source_language.upper()) if source_language else None
        self.formal = formal

        deepl_key = api_key
        if not deepl_key:
            import os
            deepl_key = os.environ.get("DEEPL_AUTH_KEY")

        self.client = deepl.Translator(deepl_key)

    def translate_caption(
        self,
        text: str,
        target_language: Optional[str] = None,
    ) -> str:
        """
        Translate a single caption string using DeepL API.

        Args:
            text: Source text to translate.
            target_language: Override target language for this translation.

        Returns:
            Translated text string.
        """
        if not text or not text.strip():
            return text

        target = DEEPL_LANGUAGE_MAP.get(target_language, target_language.upper()) if target_language else self.target_language

        try:
            result = self.client.translate_text(
                text,
                source_lang=self.source_language,
                target_lang=target,
                formal="yes" if self.formal else "no",
            )
            return result.text
        except deepl.DeepLException as e:
            logger.error(f"DeepL translation error: {e}")
            return text

    def translate_final_result(
        self,
        result: FinalTranscriptResult,
        target_language: Optional[str] = None,
    ) -> dict:
        """
        Translate a FinalTranscriptResult and return a dict with both original and translation.

        Args:
            result: FinalTranscriptResult to translate.
            target_language: Override target language.

        Returns:
            Dict with original, translated text, and metadata.
        """
        translated = self.translate_caption(result.transcript, target_language)
        return {
            "original": result.transcript,
            "translated": translated,
            "target_language": target_language or self.target_language,
            "confidence": result.confidence,
        }

    def translate_batch(
        self,
        texts: list[str],
        target_language: Optional[str] = None,
    ) -> list[str]:
        """
        Translate multiple caption strings in a single DeepL API call.

        Args:
            texts: List of source texts to translate.
            target_language: Override target language.

        Returns:
            List of translated texts.
        """
        if not texts:
            return []

        target = DEEPL_LANGUAGE_MAP.get(target_language, target_language.upper()) if target_language else self.target_language
        filtered = [t for t in texts if t and t.strip()]

        if not filtered:
            return texts

        try:
            results = self.client.translate_text(
                filtered,
                source_lang=self.source_language,
                target_lang=target,
                formal="yes" if self.formal else "no",
            )
            return [r.text for r in results]
        except deepl.DeepLException as e:
            logger.error(f"DeepL batch translation error: {e}")
            return texts


def create_translator(
    target_language: str = "es",
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
) -> LiveCaptionTranslator:
    """
    Factory function to create a DeepL LiveCaptionTranslator.

    Args:
        target_language: Target language code.
        source_language: Source language code (None for auto-detect).
        api_key: DeepL API key.

    Returns:
        Configured LiveCaptionTranslator instance.
    """
    return LiveCaptionTranslator(
        target_language=target_language,
        source_language=source_language,
        api_key=api_key,
    )
