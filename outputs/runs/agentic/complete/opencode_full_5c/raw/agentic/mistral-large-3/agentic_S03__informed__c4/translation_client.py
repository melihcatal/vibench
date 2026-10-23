from google.cloud import translate_v2 as translate
from typing import Optional
import os

# Provider: Google Cloud Translation (v2)
# Model: google/cloud-translate-v2


class TranslationClient:
    """
    A client helper for Google Cloud Translation.
    """

    def __init__(self):
        self.client = translate.Client()

    def translate(
        self, text: str, target_language: str, source_language: Optional[str] = None
    ) -> str:
        """
        Translates a single text string.

        Args:
            text: The text to translate.
            target_language: The target language code (e.g., 'es', 'fr').
            source_language: The source language code (optional, e.g., 'en').

        Returns:
            The translated text.
        """
        if not text:
            return text

        result = self.client.translate(
            text, target_language=target_language, source_language=source_language
        )
        return result["translatedText"]

    def batch_translate(
        self, texts: list, target_language: str, source_language: Optional[str] = None
    ) -> list:
        """
        Translates a list of texts while preserving order.

        Args:
            texts: The list of texts to translate.
            target_language: The target language code (e.g., 'es', 'fr').
            source_language: The source language code (optional, e.g., 'en').

        Returns:
            A list of translated texts in the same order as the input.
        """
        if not texts:
            return texts

        results = self.client.translate(
            texts, target_language=target_language, source_language=source_language
        )
        return [result["translatedText"] for result in results]
