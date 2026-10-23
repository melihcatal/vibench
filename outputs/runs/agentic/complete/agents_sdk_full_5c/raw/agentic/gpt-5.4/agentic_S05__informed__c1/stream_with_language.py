from __future__ import annotations

import asyncio
from typing import AsyncIterable, AsyncIterator

from deepgram import LiveOptions

from speech_client import build_live_options, create_deepgram_client, load_streaming_config
from speech_models import StreamingTranscriptChunk, transcript_from_deepgram_result


async def stream_with_language(
    chunks: AsyncIterable[bytes],
    *,
    language: str = "en-US",
    punctuate: bool = True,
) -> AsyncIterator[StreamingTranscriptChunk]:
    client = create_deepgram_client()
    config = load_streaming_config(language=language, punctuate=punctuate, model="nova-2")
    connection = client.listen.asynclive.v("1")
    queue: asyncio.Queue[StreamingTranscriptChunk | None] = asyncio.Queue()

    async def on_transcript(_: object, result: dict, **__: object) -> None:
        for item in transcript_from_deepgram_result(result):
            await queue.put(item)

    options = build_live_options(config)
    options["language"] = language
    options["punctuate"] = punctuate
    await connection.start(LiveOptions(**options))
    connection.on("Transcript", on_transcript)

    async def send_audio() -> None:
        try:
            async for chunk in chunks:
                if chunk:
                    await connection.send(chunk)
        finally:
            await connection.finish()
            await queue.put(None)

    sender = asyncio.create_task(send_audio())
    try:
        while True:
            event = await queue.get()
            if event is None:
                break
            yield event
    finally:
        await sender
