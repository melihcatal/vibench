import asyncio
import os
from dataclasses import dataclass
from typing import AsyncIterator, Optional

import httpx


OPENAI_AUDIO_API_URL = "https://api.openai.com/v1/audio/transcriptions"


@dataclass
class AudioChunk:
    index: int
    data: bytes


async def stream_audio_chunks(source: AsyncIterator[bytes], chunk_size: int = 65536) -> AsyncIterator[AudioChunk]:
    index = 0
    buffer = bytearray()
    async for item in source:
        buffer.extend(item)
        while len(buffer) >= chunk_size:
            yield AudioChunk(index=index, data=bytes(buffer[:chunk_size]))
            del buffer[:chunk_size]
            index += 1
    if buffer:
        yield AudioChunk(index=index, data=bytes(buffer))


async def transcribe_streamed_chunks(source: AsyncIterator[bytes], model: str = "gpt-4o-mini-transcribe") -> AsyncIterator[str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    headers = {"Authorization": f"Bearer {api_key}"}
    async with httpx.AsyncClient(timeout=60.0) as client:
        async for chunk in stream_audio_chunks(source):
            files = {"file": (f"chunk-{chunk.index}.wav", chunk.data, "audio/wav")}
            data = {"model": model}
            response = await client.post(OPENAI_AUDIO_API_URL, headers=headers, data=data, files=files)
            response.raise_for_status()
            yield response.json().get("text", "")


async def _example_source() -> AsyncIterator[bytes]:
    for _ in range(3):
        await asyncio.sleep(0)
        yield b"\x00" * 24000


async def main() -> None:
    async for text in transcribe_streamed_chunks(_example_source()):
        if text:
            print(text)


if __name__ == "__main__":
    asyncio.run(main())
