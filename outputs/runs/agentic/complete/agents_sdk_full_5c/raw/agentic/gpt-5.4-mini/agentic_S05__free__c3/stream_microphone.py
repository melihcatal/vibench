from __future__ import annotations

import asyncio
from typing import AsyncIterator

import sounddevice as sd

from speech_client import AzureStreamingSpeechClient, SpeechClientConfig
from speech_models import StreamingChunk, StreamingConfig


async def microphone_chunks(sample_rate: int = 16000, block_size: int = 3200) -> AsyncIterator[StreamingChunk]:
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[bytes | None] = asyncio.Queue()

    def callback(indata, frames, time, status) -> None:  # noqa: ANN001
        if status:
            pass
        loop.call_soon_threadsafe(queue.put_nowait, bytes(indata))

    with sd.RawInputStream(samplerate=sample_rate, blocksize=block_size, dtype="int16", channels=1, callback=callback):
        while True:
            data = await queue.get()
            if data is None:
                break
            yield StreamingChunk(audio=data)


async def stream_microphone() -> AsyncIterator[str]:
    client = AzureStreamingSpeechClient(SpeechClientConfig.from_env())
    cfg = StreamingConfig(language=client.config.language, punctuate=True)
    async for event in client.stream(microphone_chunks(), cfg):
        if event.get("text"):
            yield event["text"]


__all__ = ["stream_microphone", "microphone_chunks"]
