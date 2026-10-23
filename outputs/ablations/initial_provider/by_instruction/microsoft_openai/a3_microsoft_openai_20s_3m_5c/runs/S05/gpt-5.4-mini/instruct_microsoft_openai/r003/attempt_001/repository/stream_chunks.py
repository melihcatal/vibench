from typing import AsyncIterator, Iterable

from speech_client import stream_transcript_events
from speech_models import TranscriptChunk


async def stream_chunks(chunks: AsyncIterator[bytes]) -> AsyncIterator[TranscriptChunk]:
    async for item in stream_transcript_events(chunks):
        yield item
