from typing import AsyncIterator, Iterable

from speech_client import build_async_client
from speech_models import (
    StreamingAudioChunk,
    TranscriptEvent,
    normalize_transcript_payload,
)


async def stream_chunks(source: AsyncIterator[bytes]) -> AsyncIterator[TranscriptEvent]:
    client = build_async_client()
    async for chunk in source:
        event = await client.audio.transcriptions.create(
            model="whisper-1", file=chunk, response_format="verbose_json"
        )
        yield normalize_transcript_payload(event)


def to_audio_chunks(items: Iterable[bytes]) -> list[StreamingAudioChunk]:
    return [StreamingAudioChunk(data=item) for item in items]
