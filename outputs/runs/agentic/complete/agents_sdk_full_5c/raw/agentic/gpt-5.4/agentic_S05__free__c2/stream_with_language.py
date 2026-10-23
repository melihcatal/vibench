from __future__ import annotations

from deepgram.clients.listen.v1.websocket.async_client import AsyncListenWebSocketClient

from speech_client import build_streaming_options
from speech_models import StreamingConfig


async def start_stream_with_language(
    connection: AsyncListenWebSocketClient,
    language_code: str = "en-US",
    punctuate: bool = True,
) -> bool:
    config = StreamingConfig(
        language_code=language_code,
        punctuate=punctuate,
        model="nova-2",
        interim_results=True,
    )
    options = build_streaming_options(config)
    return await connection.start(options)
