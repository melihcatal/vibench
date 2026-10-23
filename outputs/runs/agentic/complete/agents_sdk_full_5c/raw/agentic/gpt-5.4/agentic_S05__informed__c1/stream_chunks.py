from __future__ import annotations

import asyncio
from typing import AsyncIterable, AsyncIterator

from deepgram import LiveOptions

from speech_client import build_live_options, create_deepgram_client, load_streaming_config
from speech_models import StreamingTranscriptChunk, transcript_from_deepgram_result


async def stream_audio_chunks(chunks: AsyncIterable[bytes]) -> AsyncIterator[StreamingTranscriptChunk]:
    client = create_deepgram_client()
    config = load_streaming_config()
    connection = client.listen.asynclive.v("1")
    queue: asyncio.Queue[StreamingTranscriptChunk | None] = asyncio.Queue()

    async def on_message(_: object, result: dict, **__: object) -> None:
        for transcript in transcript_from_deepgram_result(result):
            await queue.put(transcript)

    connection.on("Transcript", on_message)
    await connection.start(LiveOptions(**build_live_options(config)))

    async def produce() -> None:
        try:
            async for chunk in chunks:
                if chunk:
                    await connection.send(chunk)
        finally:
            await connection.finish()
            await queue.put(None)

    producer = asyncio.create_task(produce())
    try:
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item
    finally:
        await producer
