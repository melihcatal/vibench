import asyncio
import os
from typing import AsyncIterable, AsyncIterator

from speech_models import TranscriptEvent
from deep_translator import GoogleTranslator


async def live_caption_translate(events: AsyncIterable[TranscriptEvent], target_language: str = "es") -> AsyncIterator[TranscriptEvent]:
    translator = GoogleTranslator(source="auto", target=target_language)
    async for event in events:
        translated = translator.translate(event.text) if event.text else ""
        yield TranscriptEvent(text=translated, is_partial=event.is_partial, confidence=event.confidence, metadata={**event.metadata, "target_language": target_language})
