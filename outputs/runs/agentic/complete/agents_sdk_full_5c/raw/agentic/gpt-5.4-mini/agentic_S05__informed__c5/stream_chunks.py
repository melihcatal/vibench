from __future__ import annotations

from typing import AsyncIterable, Iterable

from speech_client import SpeechClientHelper
from speech_models import AudioChunk, TranscriptSegment


async def async_audio_chunks(source: AsyncIterable[bytes], sample_rate_hz: int = 16000) -> AsyncIterable[AudioChunk]:
    async for data in source:
        yield AudioChunk(data=data, sample_rate_hz=sample_rate_hz)


async def stream_chunks(source: AsyncIterable[bytes], language_code: str = "en-US") -> AsyncIterable[TranscriptSegment]:
    helper = SpeechClientHelper()
    async for chunk in async_audio_chunks(source, helper.config.sample_rate_hz):
        responses = helper.stream_audio([chunk], language_code=language_code)
        for response in responses:
            for segment in helper.response_to_segments(response):
                if segment.text:
                    yield segment
