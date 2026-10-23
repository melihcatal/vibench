from __future__ import annotations

import asyncio
from typing import AsyncIterator

import sounddevice as sd

from speech_client import (
    build_audio_request,
    build_config_request,
    get_google_speech_client,
)
from speech_models import (
    StreamingRecognitionConfig,
    StreamingTranscriptEvent,
    normalize_google_streaming_response,
)


async def stream_microphone_transcripts(
    config: StreamingRecognitionConfig,
    blocksize: int = 3200,
    device: int | None = None,
) -> AsyncIterator[StreamingTranscriptEvent]:
    queue: asyncio.Queue[bytes | None] = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def callback(indata, frames, time, status):
        if status:
            return
        loop.call_soon_threadsafe(queue.put_nowait, bytes(indata))

    stream = sd.RawInputStream(
        samplerate=config.sample_rate_hertz,
        channels=1,
        dtype="int16",
        blocksize=blocksize,
        device=device,
        callback=callback,
    )

    async def request_iter():
        yield build_config_request(config)
        while True:
            chunk = await queue.get()
            if chunk is None:
                break
            yield build_audio_request(chunk)

    client = get_google_speech_client()
    with stream:
        responses = await client.streaming_recognize(requests=request_iter())
        async for response in responses:
            for event in normalize_google_streaming_response(response):
                yield event
