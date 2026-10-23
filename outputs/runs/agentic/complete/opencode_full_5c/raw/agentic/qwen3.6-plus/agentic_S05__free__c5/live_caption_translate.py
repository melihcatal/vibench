import asyncio
import os
from typing import AsyncGenerator, Optional

from google.cloud.translate_v2 import Client as TranslateClient
from google.api_core.client_options import ClientOptions

from speech_models import StreamingTranscriptEvent

GOOGLE_TRANSLATE_ENDPOINT = "translation.googleapis.com"


class LiveCaptionTranslator:
    def __init__(
        self,
        target_language: str = "es",
        source_language: Optional[str] = None,
        project_id: Optional[str] = None,
    ):
        self.target_language = target_language
        self.source_language = source_language
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
        client_options = ClientOptions(api_endpoint=GOOGLE_TRANSLATE_ENDPOINT)
        self._client = TranslateClient(client_options=client_options)
        self._translation_cache: dict = {}

    def translate_text(self, text: str) -> str:
        if not text or not text.strip():
            return ""

        cache_key = (text.strip().lower(), self.target_language)
        if cache_key in self._translation_cache:
            return self._translation_cache[cache_key]

        params = {
            "q": text,
            "target": self.target_language,
            "format": "text",
        }
        if self.source_language:
            params["source"] = self.source_language

        result = self._client.translate(**params)
        translated = result.get("translatedText", text)
        self._translation_cache[cache_key] = translated
        return translated

    async def translate_event(self, event: StreamingTranscriptEvent) -> dict:
        original_text = event.text
        translated_text = self.translate_text(original_text)
        return {
            "original_text": original_text,
            "translated_text": translated_text,
            "target_language": self.target_language,
            "source_language": self.source_language or "auto",
            "is_final": event.result.is_final,
            "confidence": event.confidence,
            "timestamp": event.timestamp.isoformat(),
        }


async def live_caption_translate(
    transcript_events: AsyncGenerator[StreamingTranscriptEvent, None],
    target_language: str = "es",
    source_language: Optional[str] = None,
) -> AsyncGenerator[dict, None]:
    translator = LiveCaptionTranslator(
        target_language=target_language,
        source_language=source_language,
    )

    async for event in transcript_events:
        if event.text:
            result = await translator.translate_event(event)
            yield result


async def translate_final_captions(
    transcript_events: AsyncGenerator[StreamingTranscriptEvent, None],
    target_language: str = "fr",
) -> AsyncGenerator[str, None]:
    translator = LiveCaptionTranslator(target_language=target_language)

    async for event in transcript_events:
        if event.result.is_final and event.text:
            translated = translator.translate_text(event.text)
            yield translated
