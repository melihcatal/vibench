import asyncio
import os
from typing import AsyncIterator, Iterable

import aiohttp


OPENAI_TRANSCRIBE_URL = "https://api.openai.com/v1/audio/transcriptions"
OPENAI_MODEL = "gpt-4o-mini-transcribe"


class OpenAIAudioChunkStreamer:
    def __init__(self, source: AsyncIterator[bytes], chunk_size: int = 4096):
        self._source = source
        self._chunk_size = chunk_size

    async def stream(self) -> AsyncIterator[bytes]:
        buffer = bytearray()
        async for chunk in self._source:
            if not chunk:
                continue
            buffer.extend(chunk)
            while len(buffer) >= self._chunk_size:
                yield bytes(buffer[: self._chunk_size])
                del buffer[: self._chunk_size]
        if buffer:
            yield bytes(buffer)


async def transcribe_chunk(session: aiohttp.ClientSession, audio_chunk: bytes, filename: str) -> str:
    data = aiohttp.FormData()
    data.add_field("model", OPENAI_MODEL)
    data.add_field("file", audio_chunk, filename=filename, content_type="application/octet-stream")
    data.add_field("response_format", "text")
    async with session.post(OPENAI_TRANSCRIBE_URL, data=data) as response:
        response.raise_for_status()
        return await response.text()


async def stream_audio_chunks(source: AsyncIterator[bytes]) -> AsyncIterator[str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    headers = {"Authorization": f"Bearer {api_key}"}
    streamer = OpenAIAudioChunkStreamer(source)

    async with aiohttp.ClientSession(headers=headers) as session:
        index = 0
        async for chunk in streamer.stream():
            index += 1
            transcript = await transcribe_chunk(session, chunk, f"chunk-{index}.wav")
            yield transcript


async def _demo_source() -> AsyncIterator[bytes]:
    for part in (b"audio-part-1", b"audio-part-2", b"audio-part-3"):
        await asyncio.sleep(0)
        yield part


async def main() -> None:
    async for item in stream_audio_chunks(_demo_source()):
        print(item, flush=True)


if __name__ == "__main__":
    asyncio.run(main())
