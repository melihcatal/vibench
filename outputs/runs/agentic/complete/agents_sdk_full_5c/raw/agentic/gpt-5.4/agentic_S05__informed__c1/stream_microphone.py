from __future__ import annotations

import asyncio
from typing import AsyncIterator, Awaitable, Callable, Optional

from deepgram import LiveOptions

from speech_client import build_live_options, create_deepgram_client, load_streaming_config
from speech_models import StreamingTranscriptChunk, transcript_from_deepgram_result


async def stream_microphone(
    microphone_frames: AsyncIterator[bytes],
    on_transcript: Optional[Callable[[StreamingTranscriptChunk], Awaitable[None] | None]] = None,
) -> AsyncIterator[StreamingTranscriptChunk]:
    client = create_deepgram_client()
    config = load_streaming_config()
    connection = client.listen.asynclive.v("1")
    queue: asyncio.Queue[Optional[StreamingTranscriptChunk]] = asyncio.Queue()

    async def handle_transcript(_: object, result: dict, **__: object) -> None:
        for chunk in transcript_from_deepgram_result(result):
            await queue.put(chunk)

    connection.on("Transcript", handle_transcript)
    await connection.start(LiveOptions(**build_live_options(config)))

    async def sender() -> None:
        try:
            async for frame in microphone_frames:
                if frame:
                    await connection.send(frame)
        finally:
            await connection.finish()
            await queue.put(None)

    sender_task = asyncio.create_task(sender())
    try:
        while True:
            item = await queue.get()
            if item is None:
                break
            if on_transcript is not None:
                maybe = on_transcript(item)
                if asyncio.iscoroutine(maybe):
                    await maybe
            yield item
    finally:
        await sender_task
