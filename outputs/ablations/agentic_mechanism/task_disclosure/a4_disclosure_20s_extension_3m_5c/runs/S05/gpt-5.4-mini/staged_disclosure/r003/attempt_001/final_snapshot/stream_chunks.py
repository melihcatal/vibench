import asyncio
import os
from typing import AsyncIterator, Optional

import httpx


OPENAI_AUDIO_STREAM_URL = "https://api.openai.com/v1/audio/speech"


async def _iter_source_chunks(source: AsyncIterator[bytes], max_chunk_size: int) -> AsyncIterator[bytes]:
    buffer = bytearray()
    async for part in source:
        if not part:
            continue
        buffer.extend(part)
        while len(buffer) >= max_chunk_size:
            yield bytes(buffer[:max_chunk_size])
            del buffer[:max_chunk_size]
    if buffer:
        yield bytes(buffer)


async def stream_audio_chunks(source: AsyncIterator[bytes], chunk_size: int = 4096) -> AsyncIterator[bytes]:
    async with httpx.AsyncClient(timeout=None) as client:
        headers = {"Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY', '')}"}
        async with client.stream("POST", OPENAI_AUDIO_STREAM_URL, headers=headers) as response:
            response.raise_for_status()
            async for upstream_chunk in _iter_source_chunks(source, chunk_size):
                if upstream_chunk:
                    yield upstream_chunk
            async for chunk in response.aiter_bytes():
                if chunk:
                    yield chunk


async def stream_from_async_source(source: AsyncIterator[bytes], chunk_size: int = 4096) -> list[bytes]:
    chunks = []
    async for chunk in stream_audio_chunks(source, chunk_size=chunk_size):
        chunks.append(chunk)
    return chunks


async def _empty_source() -> AsyncIterator[bytes]:
    if False:
        yield b""


if __name__ == "__main__":
    async def _run() -> None:
        await stream_from_async_source(_empty_source())

    asyncio.run(_run())
