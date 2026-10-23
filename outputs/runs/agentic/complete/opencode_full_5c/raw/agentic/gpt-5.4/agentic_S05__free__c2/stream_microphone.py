from __future__ import annotations

import asyncio
from typing import AsyncIterator

import sounddevice as sd

from speech_client import (
    aiter_audio_requests,
    build_initial_request,
    build_streaming_config,
    get_async_speech_client,
)
from speech_models import normalize_google_streaming_response


async def microphone_audio_stream(
    sample_rate: int = 16000, blocksize: int = 1600
) -> AsyncIterator[bytes]:
    queue: asyncio.Queue[bytes] = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def callback(indata, frames, time, status):
        del frames, time
        if status:
            return
        loop.call_soon_threadsafe(queue.put_nowait, bytes(indata))

    stream = sd.RawInputStream(
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
        blocksize=blocksize,
        callback=callback,
    )
    with stream:
        while True:
            yield await queue.get()


async def stream_microphone_transcripts() -> AsyncIterator[dict[str, object]]:
    client = get_async_speech_client()
    config = build_streaming_config(sample_rate_hz=16000)

    async def request_iter() -> AsyncIterator:
        yield build_initial_request(config=config)
        async for request in aiter_audio_requests(microphone_audio_stream()):
            yield request

    responses = await client.streaming_recognize(requests=request_iter())
    async for response in responses:
        event = normalize_google_streaming_response(response)
        for result in event.results:
            if result.text:
                yield {
                    "text": result.text,
                    "is_final": result.is_final,
                    "stability": result.stability,
                    "provider": "Google Cloud Speech-to-Text V2",
                }
