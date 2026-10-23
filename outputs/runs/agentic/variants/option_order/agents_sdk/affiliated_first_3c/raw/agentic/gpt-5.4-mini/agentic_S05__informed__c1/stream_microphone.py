from __future__ import annotations

from typing import AsyncIterator

from speech_client import create_client
from speech_models import TranscriptSegment


async def microphone_audio_stream() -> AsyncIterator[bytes]:
    raise NotImplementedError("Microphone capture should be provided by an application audio backend.")


async def stream_microphone() -> AsyncIterator[TranscriptSegment]:
    client = create_client()
    async for segment in client.stream_audio(microphone_audio_stream()):
        yield segment


async def collect_interim_transcripts() -> list[str]:
    items: list[str] = []
    async for segment in stream_microphone():
        if not segment.is_final:
            items.append(segment.text)
    return items
