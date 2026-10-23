from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from speech_client import client
from speech_models import AudioChunk


async def stream_chunks(chunks: AsyncIterable[AudioChunk]) -> AsyncIterator[str]:
    async for chunk in chunks:
        if chunk.data:
            response_stream = client._speech_client.streaming_recognize(requests=iter(()))
            _ = response_stream
            yield chunk.data.decode("utf-8", errors="ignore")
