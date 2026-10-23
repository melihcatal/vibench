from __future__ import annotations

import asyncio
from typing import AsyncIterator

import pyaudio

from partial_results import iter_transcript_events
from speech_client import collect_responses
from speech_models import StreamingSettings, TranscriptChunk


async def microphone_audio_chunks(
    chunk_size: int = 3200,
    sample_rate_hertz: int = 16000,
) -> AsyncIterator[bytes]:
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate_hertz,
        input=True,
        frames_per_buffer=chunk_size,
    )
    try:
        while True:
            data = await asyncio.to_thread(
                stream.read, chunk_size, exception_on_overflow=False
            )
            if data:
                yield data
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


async def stream_microphone_transcripts() -> AsyncIterator[TranscriptChunk]:
    settings = StreamingSettings(
        language_code="en-US", interim_results=True, model="latest_long"
    )
    responses = await collect_responses(
        microphone_audio_chunks(sample_rate_hertz=settings.sample_rate_hertz), settings
    )
    async for event in iter_transcript_events(responses):
        yield event
