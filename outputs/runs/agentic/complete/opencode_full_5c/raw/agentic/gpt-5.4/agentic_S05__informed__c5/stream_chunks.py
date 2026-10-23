from __future__ import annotations

import asyncio
from typing import AsyncIterable, AsyncIterator

from speech_client import load_streaming_config, open_stream, stream_audio_chunks
from speech_models import TranscriptEvent, normalize_deepgram_result


async def stream_audio_source(
    audio_source: AsyncIterable[bytes],
) -> AsyncIterator[TranscriptEvent]:
    config = load_streaming_config()
    queue: asyncio.Queue[TranscriptEvent] = asyncio.Queue()

    async def on_transcript(result) -> None:
        event = normalize_deepgram_result(result)
        if event.transcript:
            await queue.put(event)

    connection = await open_stream(config, on_transcript)
    sender = asyncio.create_task(stream_audio_chunks(connection, audio_source))
    try:
        while True:
            yield await queue.get()
    finally:
        sender.cancel()
