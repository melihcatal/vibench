from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from partial_results import iter_transcript_events
from speech_client import collect_responses
from speech_models import StreamingSettings, TranscriptChunk


async def stream_audio_chunks(
    audio_source: AsyncIterable[bytes],
    settings: StreamingSettings | None = None,
) -> AsyncIterator[TranscriptChunk]:
    active_settings = settings or StreamingSettings(
        language_code="en-US", interim_results=True, model="latest_long"
    )
    responses = await collect_responses(audio_source, active_settings)
    async for event in iter_transcript_events(responses):
        yield event
