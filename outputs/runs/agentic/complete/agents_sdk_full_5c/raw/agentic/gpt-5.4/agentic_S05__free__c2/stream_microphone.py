from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Callable
from typing import Any

from deepgram import LiveTranscriptionEvents

from partial_results import PartialResultsHandler
from speech_client import create_async_client
from speech_models import StreamingConfig


async def stream_microphone_audio(
    microphone_source: Callable[[], AsyncIterator[bytes]],
    api_key: str,
) -> AsyncIterator[str]:
    client = create_async_client(api_key)
    connection = client.listen.asynclive.v("1")
    handler = PartialResultsHandler()
    queue: asyncio.Queue[str | None] = asyncio.Queue()

    @connection.on(LiveTranscriptionEvents.Transcript)
    async def _on_transcript(result: dict[str, Any], **_: Any) -> None:
        segment = handler.handle_deepgram_message(result)
        if segment and segment.text:
            await queue.put(segment.text)

    options = {
        "model": StreamingConfig().model,
        "language": "en-US",
        "encoding": "linear16",
        "sample_rate": 16000,
        "interim_results": True,
        "smart_format": True,
    }
    await connection.start(options)

    async def _pump() -> None:
        try:
            async for frame in microphone_source():
                await connection.send(frame)
        finally:
            await connection.finish()
            await queue.put(None)

    producer = asyncio.create_task(_pump())
    try:
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item
    finally:
        await producer
