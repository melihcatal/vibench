from __future__ import annotations

from typing import AsyncIterator, Iterable

from speech_client import AzureStreamingSpeechClient, SpeechClientConfig
from speech_models import StreamingChunk, StreamingConfig


async def stream_chunks(source: AsyncIterator[bytes] | Iterable[bytes]) -> AsyncIterator[dict[str, str | bool]]:
    client = AzureStreamingSpeechClient(SpeechClientConfig.from_env())
    cfg = StreamingConfig(language=client.config.language, punctuate=True)

    async def iterator() -> AsyncIterator[StreamingChunk]:
        if hasattr(source, "__aiter__"):
            async for chunk in source:  # type: ignore[attr-defined]
                yield StreamingChunk(audio=chunk)
        else:
            for chunk in source:
                yield StreamingChunk(audio=chunk)

    async for event in client.stream(iterator(), cfg):
        yield {"text": event.get("text", ""), "is_final": bool(event.get("is_final", False))}
