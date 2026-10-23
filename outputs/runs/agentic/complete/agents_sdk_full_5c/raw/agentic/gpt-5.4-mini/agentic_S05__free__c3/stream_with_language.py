from __future__ import annotations

from typing import AsyncIterator

from speech_client import AzureStreamingSpeechClient, SpeechClientConfig
from speech_models import StreamingChunk, StreamingConfig


async def stream_with_language(language: str = "en-US", punctuate: bool = True, chunks: AsyncIterator[bytes] | None = None) -> AsyncIterator[str]:
    client = AzureStreamingSpeechClient(SpeechClientConfig.from_env())
    cfg = StreamingConfig(language=language, punctuate=punctuate)

    async def chunk_source() -> AsyncIterator[StreamingChunk]:
        if chunks is None:
            return
        async for chunk in chunks:
            yield StreamingChunk(audio=chunk)

    async for event in client.stream(chunk_source(), cfg):
        if event.get("text"):
            yield event["text"]
