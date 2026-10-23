from __future__ import annotations

import asyncio
import os
from typing import Any, AsyncIterable, Awaitable, Callable, Optional

from deepgram import AsyncListenWebSocketClient, DeepgramClient, DeepgramClientOptions

from speech_models import StreamingConfig


AudioChunkSource = AsyncIterable[bytes]
EventHandler = Callable[[Any], Awaitable[None]]


def load_streaming_config(
    language_code: str = "en-US",
    sample_rate_hz: int = 16000,
    interim_results: bool = True,
    punctuate: bool = True,
) -> StreamingConfig:
    return StreamingConfig(
        sample_rate_hz=sample_rate_hz,
        language_code=language_code,
        interim_results=interim_results,
        punctuate=punctuate,
    )


def create_deepgram_client(api_key: Optional[str] = None) -> DeepgramClient:
    resolved_key = api_key or os.getenv("DEEPGRAM_API_KEY")
    if not resolved_key:
        raise ValueError("DEEPGRAM_API_KEY is required")
    options = DeepgramClientOptions(api_key=resolved_key)
    return DeepgramClient(api_key=resolved_key, config=options)


async def open_stream(
    config: StreamingConfig,
    on_transcript: EventHandler,
    api_key: Optional[str] = None,
) -> AsyncListenWebSocketClient:
    client = create_deepgram_client(api_key=api_key)
    connection = client.listen.asynclive.v("1")
    await connection.on("Transcript", on_transcript)
    await connection.start(
        {
            "model": "nova-2-general",
            "language": config.language_code,
            "encoding": config.encoding,
            "channels": config.channels,
            "sample_rate": config.sample_rate_hz,
            "interim_results": config.interim_results,
            "punctuate": config.punctuate,
            "smart_format": True,
        }
    )
    return connection


async def stream_audio_chunks(
    connection: AsyncListenWebSocketClient, source: AudioChunkSource
) -> None:
    async for chunk in source:
        if chunk:
            await connection.send(chunk)
    await asyncio.sleep(0)
    await connection.finish()
