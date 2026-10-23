from typing import AsyncIterable, AsyncIterator


async def stream_chunks(source: AsyncIterable[bytes], chunk_size: int = 4096) -> AsyncIterator[bytes]:
    async for chunk in source:
        if not isinstance(chunk, (bytes, bytearray, memoryview)):
            raise TypeError("source must yield bytes-like chunks")
        data = bytes(chunk)
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        for index in range(0, len(data), chunk_size):
            yield data[index:index + chunk_size]
