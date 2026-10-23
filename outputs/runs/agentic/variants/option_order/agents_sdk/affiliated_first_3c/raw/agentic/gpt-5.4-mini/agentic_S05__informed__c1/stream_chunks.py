from __future__ import annotations

from typing import AsyncIterator, Iterable

from speech_client import create_client
from speech_models import TranscriptSegment


async def stream_chunks(chunks: AsyncIterator[bytes], language_code: str = "en-US") -> AsyncIterator[TranscriptSegment]:
    client = create_client()
    async for segment in client.stream_audio(chunks, language_code=language_code):
        yield segment


async def stream_chunk_iterable(chunks: Iterable[bytes]) -> list[str]:
    async def gen() -> AsyncIterator[bytes]:
        for chunk in chunks:
            yield chunk

    transcripts: list[str] = []
    async for segment in stream_chunks(gen()):
        transcripts.append(segment.text)
    return transcripts
