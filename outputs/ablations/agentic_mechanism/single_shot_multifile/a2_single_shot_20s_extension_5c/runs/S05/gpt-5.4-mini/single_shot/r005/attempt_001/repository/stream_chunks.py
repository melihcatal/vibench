import asyncio
from typing import AsyncIterable, AsyncIterator, Optional

from speech_client import get_speech_client
from speech_models import AudioChunk, TranscriptEvent


async def stream_chunks(chunks: AsyncIterable[AudioChunk], language_code: str = "en-US") -> AsyncIterator[TranscriptEvent]:
    client = get_speech_client()
    async for event in client.stream_chunks(chunks, language_code=language_code):
        yield event


async def main() -> None:
    async def source() -> AsyncIterator[AudioChunk]:
        yield AudioChunk(audio=b"", is_final=True)

    async for event in stream_chunks(source()):
        print(event.text)


if __name__ == "__main__":
    asyncio.run(main())
