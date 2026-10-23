import asyncio
import os
from typing import AsyncIterator, Callable, Optional

import httpx


OPENAI_AUDIO_TRANSCRIPTION_URL = "https://api.openai.com/v1/audio/transcriptions"


async def stream_audio_chunks(
    source: AsyncIterator[bytes],
    on_chunk: Optional[Callable[[bytes], None]] = None,
    chunk_size: int = 4096,
) -> None:
    api_key = os.environ["OPENAI_API_KEY"]
    headers = {"Authorization": f"Bearer {api_key}"}
    buffer = bytearray()

    async with httpx.AsyncClient(timeout=60.0, headers=headers) as client:
        async for data in source:
            buffer.extend(data)
            while len(buffer) >= chunk_size:
                chunk = bytes(buffer[:chunk_size])
                del buffer[:chunk_size]
                if on_chunk is not None:
                    on_chunk(chunk)
                await client.post(
                    OPENAI_AUDIO_TRANSCRIPTION_URL,
                    data={"model": "whisper-1"},
                    files={"file": ("chunk.wav", chunk, "audio/wav")},
                )

        if buffer:
            chunk = bytes(buffer)
            if on_chunk is not None:
                on_chunk(chunk)
            await client.post(
                OPENAI_AUDIO_TRANSCRIPTION_URL,
                data={"model": "whisper-1"},
                files={"file": ("chunk.wav", chunk, "audio/wav")},
            )


async def _main() -> None:
    async def source() -> AsyncIterator[bytes]:
        yield b"\x00" * 8192
        yield b"\x01" * 2048

    await stream_audio_chunks(source())


if __name__ == "__main__":
    asyncio.run(_main())
