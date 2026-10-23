from __future__ import annotations

import asyncio
from typing import AsyncIterable, AsyncIterator, Iterable

from google.cloud import speech

from speech_client import create_speech_client, load_config, streaming_config


async def iter_audio_chunks(source: AsyncIterable[bytes]) -> AsyncIterator[bytes]:
    async for chunk in source:
        yield chunk


async def stream_chunks(source: AsyncIterable[bytes]) -> AsyncIterator[str]:
    client = create_speech_client()
    cfg = load_config()

    async def request_iter() -> AsyncIterator[speech.StreamingRecognizeRequest]:
        async for chunk in iter_audio_chunks(source):
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    loop = asyncio.get_running_loop()
    responses = await loop.run_in_executor(
        None,
        lambda: client.streaming_recognize(streaming_config(cfg), request_iter()),
    )
    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
