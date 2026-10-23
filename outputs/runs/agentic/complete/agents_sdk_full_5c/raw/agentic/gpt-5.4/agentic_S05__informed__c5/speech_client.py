from __future__ import annotations

import os
from typing import Any, AsyncIterable

from deepgram import (
    AsyncListenWebSocketClient,
    DeepgramClient,
    LiveOptions,
)

from speech_models import StreamingOptions


DEEPGRAM_API_KEY_ENV = "DEEPGRAM_API_KEY"
DEEPGRAM_MODEL = "nova-2"
DEEPGRAM_LISTEN_VERSION = "1"


class DeepgramStreamingHelper:
    def __init__(self, options: StreamingOptions | None = None) -> None:
        self.options = options or StreamingOptions(model=DEEPGRAM_MODEL)

    @staticmethod
    def get_api_key() -> str:
        api_key = os.getenv(DEEPGRAM_API_KEY_ENV)
        if not api_key:
            raise RuntimeError(f"Missing required environment variable: {DEEPGRAM_API_KEY_ENV}")
        return api_key

    def create_client(self) -> DeepgramClient:
        return DeepgramClient(self.get_api_key())

    def build_live_options(self, **overrides: Any) -> LiveOptions:
        opts = {
            "model": self.options.model,
            "language": self.options.language_code,
            "smart_format": self.options.punctuate,
            "punctuate": self.options.punctuate,
            "interim_results": self.options.interim_results,
            "sample_rate": self.options.sample_rate_hz,
            "encoding": self.options.encoding,
            "channels": self.options.channels,
        }
        opts.update(self.options.extra)
        opts.update(overrides)
        return LiveOptions(**opts)

    async def open_connection(self, **overrides: Any) -> AsyncListenWebSocketClient:
        client = self.create_client()
        connection = client.listen.asyncwebsocket.v(DEEPGRAM_LISTEN_VERSION)
        started = await connection.start(self.build_live_options(**overrides))
        if not started:
            raise RuntimeError("Failed to start Deepgram Streaming API websocket")
        return connection


async def stream_async_bytes(connection: AsyncListenWebSocketClient, source: AsyncIterable[bytes]) -> None:
    async for chunk in source:
        if chunk:
            await connection.send(chunk)
    await connection.finish()
