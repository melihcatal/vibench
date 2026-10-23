from __future__ import annotations

import asyncio
import os
from typing import AsyncIterable, AsyncIterator, Optional

from deepgram import AsyncDeepgramClient
from deepgram.clients.listen.v1.websocket.options import LiveOptions

from speech_models import StreamingAudioChunk


DEFAULT_DEEPGRAM_MODEL = os.getenv("DEEPGRAM_MODEL", "nova-2")
DEFAULT_LANGUAGE = os.getenv("DEEPGRAM_LANGUAGE", "en-US")
DEFAULT_SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE_HZ", "16000"))


def get_deepgram_client(api_key: Optional[str] = None) -> AsyncDeepgramClient:
    key = api_key or os.getenv("DEEPGRAM_API_KEY")
    if not key:
        raise RuntimeError("DEEPGRAM_API_KEY is required")
    return AsyncDeepgramClient(api_key=key)


def build_live_options(
    *,
    language: str = DEFAULT_LANGUAGE,
    model: str = DEFAULT_DEEPGRAM_MODEL,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    interim_results: bool = True,
    punctuate: bool = True,
    smart_format: bool = True,
    encoding: str = "linear16",
    channels: int = 1,
) -> LiveOptions:
    return LiveOptions(
        model=model,
        language=language,
        encoding=encoding,
        channels=channels,
        sample_rate=sample_rate,
        interim_results=interim_results,
        punctuate=punctuate,
        smart_format=smart_format,
    )


async def send_audio_chunks(
    connection,
    chunks: AsyncIterable[bytes | StreamingAudioChunk],
) -> None:
    async for chunk in chunks:
        payload = chunk.data if isinstance(chunk, StreamingAudioChunk) else chunk
        if payload:
            await connection.send(payload)
    await connection.finish()


async def queue_to_audio_chunks(
    queue: "asyncio.Queue[Optional[bytes]]",
) -> AsyncIterator[bytes]:
    while True:
        item = await queue.get()
        if item is None:
            break
        yield item
