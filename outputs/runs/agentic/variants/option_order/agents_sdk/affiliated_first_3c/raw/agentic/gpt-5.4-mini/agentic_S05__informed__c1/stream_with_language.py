from __future__ import annotations

from typing import AsyncIterator

from speech_client import create_client
from speech_models import StreamingSpeechConfig, TranscriptSegment


async def stream_with_language(audio_chunks: AsyncIterator[bytes], language_code: str, enable_punctuation: bool = True) -> AsyncIterator[TranscriptSegment]:
    client = create_client()
    async for segment in client.stream_audio(audio_chunks, language_code=language_code, punctuation=enable_punctuation):
        yield segment


async def start_recognizer(language_code: str = "en-US", enable_punctuation: bool = True) -> StreamingSpeechConfig:
    return StreamingSpeechConfig(language_code=language_code, enable_punctuation=enable_punctuation)
