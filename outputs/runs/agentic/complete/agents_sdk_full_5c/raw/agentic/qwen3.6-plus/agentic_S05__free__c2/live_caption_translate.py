"""
Translate live captions into another language using Google Cloud Translation API.

This module consumes live transcript captions and translates them in real time
using the Google Cloud Translation API (translate.googleapis.com) via the
google-cloud-translate SDK. Supports automatic source language detection and
target language specification.
"""

import asyncio
import logging
from typing import AsyncIterator, Optional

from google.cloud.translate_v2 import Client as TranslateClient
from google.cloud.translate_v3 import TranslationServiceClient

logger = logging.getLogger(__name__)

GOOGLE_TRANSLATE_API_ENDPOINT = "translate.googleapis.com"
GOOGLE_TRANSLATE_V3_ENDPOINT = "translation.googleapis.com"


class LiveCaptionTranslator:
    """
    Translate live speech-to-text captions using Google Cloud Translation.

    Uses the google-cloud-translate SDK to send caption text to
    translate.googleapis.com and receive translated results.
    """

    def __init__(
        self,
        target_language: str = "es",
        source_language: Optional[str] = None,
        project_id: Optional[str] = None,
        location: str = "global",
        model: str = "nmt",
    ):
        """
        Initialize the live caption translator.

        Args:
            target_language: BCP-47 target language code (e.g., 'es' for Spanish).
            source_language: BCP-47 source language code or None for auto-detect.
            project_id: Google Cloud project ID for Translation v3 API.
            location: Google Cloud location for the translation resource.
            model: Translation model to use ('nmt' for Neural Machine Translation).
        """
        self._target_language = target_language
        self._source_language = source_language
        self._project_id = project_id
        self._location = location
        self._model = model
        self._translate_client = TranslateClient()
        logger.info(
            "LiveCaptionTranslator initialized for target=%s via %s",
            target_language,
            GOOGLE_TRANSLATE_API_ENDPOINT,
        )

    def translate_caption(self, caption_text: str) -> dict:
        """
        Translate a single caption string using Google Cloud Translation API.

        Args:
            caption_text: Source language caption text to translate.

        Returns:
            dict with keys:
                - 'original': Original caption text
                - 'translated': Translated caption text
                - 'source_language': Detected or specified source language
                - 'target_language': Target language code
                - 'model': Translation model used
        """
        if not caption_text or not caption_text.strip():
            return {
                "original": caption_text,
                "translated": "",
                "source_language": self._source_language or "auto",
                "target_language": self._target_language,
                "model": self._model,
            }

        kwargs = {
            "target_language": self._target_language,
        }
        if self._source_language:
            kwargs["source_language"] = self._source_language

        result = self._translate_client.translate(caption_text, **kwargs)

        translated_text = result.get("translatedText", "")
        detected_source = result.get(
            "detectedSourceLanguage",
            self._source_language or "unknown",
        )

        logger.debug(
            "Translated via %s [%s -> %s]: %s -> %s",
            GOOGLE_TRANSLATE_API_ENDPOINT,
            detected_source,
            self._target_language,
            caption_text[:80],
            translated_text[:80],
        )

        return {
            "original": caption_text,
            "translated": translated_text,
            "source_language": detected_source,
            "target_language": self._target_language,
            "model": self._model,
        }

    def translate_batch(self, captions: list[str]) -> list[dict]:
        """
        Translate a batch of caption strings in a single API call.

        Args:
            captions: List of caption text strings to translate.

        Returns:
            List of translation result dicts.
        """
        if not captions:
            return []

        kwargs = {
            "target_language": self._target_language,
        }
        if self._source_language:
            kwargs["source_language"] = self._source_language

        results = self._translate_client.translate(captions, **kwargs)

        translated_results = []
        for i, result in enumerate(results):
            translated_results.append({
                "original": captions[i],
                "translated": result.get("translatedText", ""),
                "source_language": result.get(
                    "detectedSourceLanguage",
                    self._source_language or "unknown",
                ),
                "target_language": self._target_language,
                "model": self._model,
            })

        return translated_results


async def stream_translated_captions(
    caption_stream: AsyncIterator[dict],
    target_language: str = "es",
    source_language: Optional[str] = None,
    project_id: Optional[str] = None,
) -> AsyncIterator[dict]:
    """
    Consume a stream of live captions and yield translated versions.

    Args:
        caption_stream: Async iterator yielding caption dicts with a 'text' key.
        target_language: Target BCP-47 language code.
        source_language: Source BCP-47 language code (None for auto-detect).
        project_id: Google Cloud project ID.

    Yields:
        dict: Translation result with original and translated text.
    """
    translator = LiveCaptionTranslator(
        target_language=target_language,
        source_language=source_language,
        project_id=project_id,
    )

    async for caption in caption_stream:
        text = caption.get("text", "")
        if not text.strip():
            continue

        translation = translator.translate_caption(text)
        translation["is_final"] = caption.get("is_final", False)
        translation["confidence"] = caption.get("confidence", 0.0)

        yield translation
