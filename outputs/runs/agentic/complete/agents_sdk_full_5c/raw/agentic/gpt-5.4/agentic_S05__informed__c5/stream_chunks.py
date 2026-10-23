from __future__ import annotations

import asyncio
from typing import AsyncIterable, AsyncIterator, Callable, Optional

from deepgram import LiveTranscriptionEvents

from partial_results import DeepgramPartialResultsHandler
from speech_client import DeepgramStreamingHelper
from speech_models import TranscriptChunk


async def stream_audio_chunks(
    chunk_source: AsyncIterable[bytes],
    *,
    on_transcript: Optional[Callable[[TranscriptChunk], None]] = None,
) -> AsyncIterator[TranscriptChunk]:
    helper = DeepgramStreamingHelper()
    connection = await helper.open_connection()
    queue: asyncio.Queue[TranscriptChunk | None] = asyncio.Queue()
    handler = DeepgramPartialResultsHandler()

    async def on_message(_: object, result: object, **__: object) -> None:
        chunk = handler.handle_result(result)
        if chunk is not None:
            if on_transcript is not None:
                on_transcript(chunk)
            await queue.put(chunk)

    async def on_close(_: object, **__: object) -> None:
        await queue.put(None)

    connection.on(LiveTranscriptionEvents.Transcript, on_message)
    connection.on(LiveTranscriptionEvents.Close, on_close)

    sender = asyncio.create_task(_send_chunks(connection, chunk_source))
    try:
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item
    finally:
        if not sender.done():
            sender.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await sender


async def _send_chunks(connection: object, chunk_source: AsyncIterable[bytes]) -> None:
    async for chunk in chunk_source:
        if chunk:
            await connection.send(chunk)
    await connection.finish()


import contextlib
