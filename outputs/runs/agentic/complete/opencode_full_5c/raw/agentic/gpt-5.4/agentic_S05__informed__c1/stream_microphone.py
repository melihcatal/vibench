from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

from stream_chunks import stream_audio_chunks
from speech_client import load_streaming_config
from speech_models import TranscriptEvent


async def stream_microphone_audio(
    microphone_source: AsyncIterator[bytes],
    *,
    language: str = "en-US",
    punctuate: bool = True,
) -> AsyncIterator[TranscriptEvent]:
    config = load_streaming_config(
        language=language, punctuate=punctuate, interim_results=True
    )
    async for event in stream_audio_chunks(microphone_source, config=config):
        yield event


async def yield_interim_transcripts(
    microphone_source: AsyncIterator[bytes],
    *,
    language: str = "en-US",
) -> AsyncIterator[str]:
    async for event in stream_microphone_audio(microphone_source, language=language):
        if event.text:
            yield event.text
        await asyncio.sleep(0)
