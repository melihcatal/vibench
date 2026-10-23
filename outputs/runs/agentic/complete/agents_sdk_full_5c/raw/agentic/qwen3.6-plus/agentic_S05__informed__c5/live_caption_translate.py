"""Translates live captions into another language using DeepL API."""

import os
from typing import Optional
import deepl
from speech_models import StreamingSpeechResult


DEEPL_API_URL = "https://api-free.deepl.com/v2"
DEEPL_API_URL_PAID = "https://api.deepl.com/v2"


class CaptionTranslator:
    """
    Translates live caption text using DeepL API.

    Uses deepl SDK (deepgram-sdk alternative not applicable; using deepl Python SDK).
    Requires DEEPL_AUTH_KEY environment variable.
    API endpoint: api.deepl.com or api-free.deepl.com.
    """

    def __init__(
        self,
        target_language: str = "ES",
        source_language: Optional[str] = None,
        auth_key: Optional[str] = None,
        use_free_api: bool = False,
    ):
        self.target_language = target_language
        self.source_language = source_language
        api_key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
        if not api_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable is required")
        server_url = DEEPL_API_URL if use_free_api else DEEPL_API_URL_PAID
        self.client = deepl.Translator(api_key, server_url=server_url)

    def translate_text(self, text: str) -> str:
        """Translate a single text string using DeepL API via deepl.Translator."""
        if not text.strip():
            return text
        kwargs = {"target_lang": self.target_language}
        if self.source_language:
            kwargs["source_lang"] = self.source_language
        result = self.client.translate_text(text, **kwargs)
        return result.text

    def translate_result(self, result: StreamingSpeechResult) -> StreamingSpeechResult:
        """Translate a streaming speech result and return a new result with translated text."""
        translated = self.translate_text(result.transcript)
        alternatives = list(result.alternatives)
        if alternatives:
            alternatives[0] = alternatives[0].__class__(
                text=translated,
                confidence=alternatives[0].confidence,
                words=alternatives[0].words,
            )
        return StreamingSpeechResult(
            is_final=result.is_final,
            stability=result.stability,
            alternatives=alternatives,
            language_code=self.target_language.lower(),
        )

    def translate_batch(self, texts: list[str]) -> list[str]:
        """Translate multiple texts in a batch request to DeepL API."""
        if not texts:
            return []
        kwargs = {"target_lang": self.target_language}
        if self.source_language:
            kwargs["source_lang"] = self.source_language
        results = self.client.translate_text(texts, **kwargs)
        return [r.text for r in results]


def create_caption_translator(
    target_language: str = "ES",
    source_language: Optional[str] = None,
) -> CaptionTranslator:
    """Factory to create a CaptionTranslator using DeepL API with DEEPL_AUTH_KEY."""
    return CaptionTranslator(
        target_language=target_language,
        source_language=source_language,
    )
