from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from partial_results import iter_transcript_events
from speech_client import collect_responses
from speech_models import StreamingSettings, TranscriptChunk


async def stream_with_language(
    audio_source: AsyncIterable[bytes],
    language_code: str,
    enable_automatic_punctuation: bool = True,
) -> AsyncIterator[TranscriptChunk]:
    settings = StreamingSettings(
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        interim_results=True,
        model="latest_long",
    )
    responses = await collect_responses(audio_source, settings)
    async for event in iter_transcript_events(responses):
        yield event
