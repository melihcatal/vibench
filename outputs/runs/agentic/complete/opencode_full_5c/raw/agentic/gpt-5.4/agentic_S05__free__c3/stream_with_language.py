from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from speech_models import StreamingRecognitionConfig, StreamingTranscriptEvent
from stream_chunks import stream_audio_chunks


async def stream_with_language_settings(
    source: AsyncIterable[bytes],
    language_code: str,
    enable_automatic_punctuation: bool = True,
    sample_rate_hertz: int = 16000,
) -> AsyncIterator[StreamingTranscriptEvent]:
    config = StreamingRecognitionConfig(
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
        enable_automatic_punctuation=enable_automatic_punctuation,
        interim_results=True,
    )
    async for event in stream_audio_chunks(source, config):
        yield event
