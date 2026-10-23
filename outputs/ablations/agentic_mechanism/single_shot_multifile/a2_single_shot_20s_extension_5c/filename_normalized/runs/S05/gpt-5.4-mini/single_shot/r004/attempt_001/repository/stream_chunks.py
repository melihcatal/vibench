import asyncio
from typing import AsyncIterable, AsyncIterator, Optional

from deepgram import LiveOptions

from speech_client import build_deepgram_client, load_speech_config
from speech_models import TranscriptEvent, normalize_transcript_event


async def stream_chunks(chunks: AsyncIterable[bytes]) -> AsyncIterator[TranscriptEvent]:
    config = load_speech_config()
    client = build_deepgram_client()
    connection = client.listen.websocket.v("1")
    options = LiveOptions(
        model=config.model,
        language=config.language,
        punctuate=config.punctuate,
        interim_results=True,
        smart_format=True,
    )
    await connection.start(options)
    try:
        async for chunk in chunks:
            if chunk:
                await connection.send(chunk)
        await connection.finish()
    finally:
        pass


async def stream_chunks_with_events(chunks: AsyncIterable[bytes]) -> AsyncIterator[TranscriptEvent]:
    queue: asyncio.Queue[TranscriptEvent] = asyncio.Queue()
    client = build_deepgram_client()
    config = load_speech_config()
    connection = client.listen.websocket.v("1")
    options = LiveOptions(
        model=config.model,
        language=config.language,
        punctuate=config.punctuate,
        interim_results=True,
        endpointing=config.endpointing,
        smart_format=True,
    )

    def on_message(_self, result, **kwargs):
        event = normalize_transcript_event(result)
        if event is not None:
            queue.put_nowait(event)

    connection.on("Transcript", on_message)
    await connection.start(options)
    async for chunk in chunks:
        if chunk:
            await connection.send(chunk)
        while not queue.empty():
            yield await queue.get()
    await connection.finish()

